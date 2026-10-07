from app.services.ingest import chunk_text
from app.services.llm import fake_embed


def test_chunk_text_non_empty():
    text = "A" * 2000
    chunks = chunk_text(text)
    assert len(chunks) >= 2
    assert all(chunks)


def test_fake_embed_dim():
    v = fake_embed("bảo hành 24 tháng", dim=384)
    assert len(v) == 384
    # unit-ish
    n = sum(x * x for x in v) ** 0.5
    assert 0.99 <= n <= 1.01
