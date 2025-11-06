"""
OpenAI-based implementations of base models.
"""
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI
import tiktoken
from tenacity import retry, stop_after_attempt, wait_exponential

from ..core.base_models import BaseEmbeddingModel, BaseSummarizationModel, BaseQAModel, BaseChunker


class OpenAIEmbeddingModel(BaseEmbeddingModel):
    """OpenAI embedding model implementation."""
    
    def __init__(self, model: str = "text-embedding-3-small", api_key: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_embedding(self, text: str) -> np.ndarray:
        """Create embedding for given text."""
        if not text or not text.strip():
            raise ValueError("Cannot create embedding for empty text")
        
        try:
            response = self.client.embeddings.create(
                input=text.strip(),
                model=self.model
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"Error creating embedding: {e}")
            print(f"Text length: {len(text)}, Text preview: {text[:100]}...")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for multiple texts."""
        # Filter out empty texts and strip whitespace
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        
        if not valid_texts:
            raise ValueError("Cannot create embeddings for empty text list")
        
        if len(valid_texts) != len(texts):
            print(f"Warning: Filtered out {len(texts) - len(valid_texts)} empty texts")
        
        try:
            response = self.client.embeddings.create(
                input=valid_texts,
                model=self.model
            )
            embeddings = [np.array(item.embedding) for item in response.data]
            return np.array(embeddings)
        except Exception as e:
            print(f"Error creating embeddings: {e}")
            print(f"Number of texts: {len(valid_texts)}")
            print(f"Text lengths: {[len(t) for t in valid_texts[:5]]}...")
            raise


class OpenAISummarizationModel(BaseSummarizationModel):
    """OpenAI-based summarization model."""
    
    def __init__(self, model: str = "gpt-4-turbo-preview", api_key: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def summarize(self, texts: List[str], max_tokens: int = 200) -> str:
        """Summarize a list of text chunks with financial context awareness."""
        combined_text = "\n\n".join(texts)
        
        prompt = f"""You are a financial document summarization expert. 
Summarize the following financial text chunks, preserving key financial information such as:
- Monetary amounts and percentages
- Dates and time periods
- Company names and entities
- Financial metrics and KPIs
- Important trends or changes

Text to summarize:
{combined_text}

Provide a concise summary in {max_tokens} tokens or less."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a financial document summarization expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        
        return response.choices[0].message.content


class OpenAIQAModel(BaseQAModel):
    """OpenAI-based QA model for financial questions."""
    
    def __init__(self, model: str = "gpt-4o-mini-realtime-preview", api_key: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def answer_question(self, context: str, question: str) -> Dict[str, Any]:
        """Answer a financial question given context."""
        prompt = f"""You are a financial analyst assistant. Answer the following question based ONLY on the provided context.

Context:
{context}

Question: {question}

Instructions:
1. Provide a clear, concise answer based on the context
2. If the answer involves financial figures, cite them accurately
3. If the context doesn't contain enough information, say so
4. Include relevant supporting details from the context

Answer:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a financial analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        return {
            "answer": answer,
            "context": context,
            "question": question
        }


class FinancialChunker(BaseChunker):
    """Financial document aware chunker."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50, model: str = "gpt-4"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.encoding_for_model(model)
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Chunk text with financial context awareness."""
        # Tokenize text
        tokens = self.encoding.encode(text)
        chunks = []
        
        # Validate chunk overlap
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(f"chunk_overlap ({self.chunk_overlap}) must be less than chunk_size ({self.chunk_size})")
        
        start = 0
        chunk_id = 0
        
        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            # Try to break at sentence boundaries
            if end < len(tokens):
                # Look for sentence endings
                for offset in range(min(50, end - start)):
                    if chunk_text[-(offset+1):].strip().endswith(('.', '!', '?', '\n')):
                        chunk_text = chunk_text[:-(offset)]
                        break
            
            chunks.append({
                "text": chunk_text.strip(),
                "chunk_id": chunk_id,
                "start_token": start,
                "end_token": end
            })
            
            chunk_id += 1
            # Ensure we always move forward to prevent infinite loop
            start = max(end - self.chunk_overlap, start + 1)
            
            # Safety check: prevent infinite loop if something goes wrong
            if start >= len(tokens):
                break
        
        return chunks
