# Ollama Setup Guide

Ollama lets you run large language models locally on your computer - completely FREE!

## Why Ollama?

✅ **Completely free** - No API costs
✅ **Private** - Your data never leaves your computer  
✅ **Fast** - No network latency
✅ **No rate limits** - Use as much as you want

## Installation

### Windows

1. Download Ollama from [ollama.ai/download](https://ollama.ai/download)

2. Run the installer

3. Ollama will start automatically in the background

### macOS

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or download from [ollama.ai/download](https://ollama.ai/download)

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Installing a Model

After installation, pull a model:

### Recommended: Llama 2 (Good balance of quality and speed)

```bash
ollama pull llama2
```

### Other Options:

```bash
# Smaller, faster (good for testing)
ollama pull llama2:7b

# Larger, better quality (if you have 16GB+ RAM)
ollama pull llama2:13b

# Mistral (alternative, also very good)
ollama pull mistral

# Code-focused (good for technical discussions)
ollama pull codellama
```

## Verifying Installation

Test that Ollama is working:

```bash
ollama list
```

You should see your installed models.

Try a simple query:

```bash
ollama run llama2 "Write a professional email reply"
```

## Running Ollama as a Service

Ollama runs as a background service automatically.

Check if it's running:

```bash
# Windows (PowerShell)
Get-Process ollama

# macOS/Linux
ps aux | grep ollama
```

If it's not running:

```bash
# Start Ollama server
ollama serve
```

## Configuration

The AI Recruiter Agent will automatically connect to Ollama at:
- **URL:** `http://localhost:11434`
- **Model:** `llama2` (default)

To use a different model, edit your `env.example`:

```bash
OLLAMA_MODEL=mistral  # or codellama, llama2:13b, etc.
```

## System Requirements

### Minimum (for llama2:7b):
- 8GB RAM
- 10GB free disk space

### Recommended (for llama2:13b):
- 16GB RAM
- 15GB free disk space

### Optimal (for larger models):
- 32GB+ RAM
- 20GB+ free disk space
- GPU (optional, speeds up processing)

## GPU Acceleration (Optional)

Ollama automatically uses your GPU if available:

- **NVIDIA GPU:** Works out of the box (CUDA)
- **Apple Silicon (M1/M2/M3):** Works out of the box (Metal)
- **AMD GPU:** Limited support

Check GPU usage:

```bash
# NVIDIA
nvidia-smi

# macOS
Activity Monitor > GPU tab
```

## Performance Tips

1. **Close other apps** - LLMs need RAM

2. **Use smaller models** for testing:
   ```bash
   ollama pull phi    # Only 2.7GB
   ```

3. **Warm up the model** before first use:
   ```bash
   ollama run llama2 "Hello"
   ```

4. **Keep Ollama running** - Starting/stopping is slow

## Troubleshooting

### "connection refused" error

Ollama isn't running. Start it:

```bash
ollama serve
```

### Model takes forever to respond

Your system might not have enough RAM. Try a smaller model:

```bash
ollama pull phi
# Then in env.example: OLLAMA_MODEL=phi
```

### "model not found"

Pull the model first:

```bash
ollama pull llama2
```

### Out of memory

Close other applications or use a smaller model.

## Comparing to Paid APIs

| Feature | Ollama (Free) | OpenAI GPT-4 | Claude |
|---------|---------------|--------------|--------|
| Cost | $0 | ~$0.03/1K tokens | ~$0.015/1K tokens |
| Speed | Fast (local) | Medium (API) | Medium (API) |
| Privacy | Complete | Data sent to OpenAI | Data sent to Anthropic |
| Quality | Good | Excellent | Excellent |
| Limits | None | Rate limits | Rate limits |

**For job hunting:** Ollama is perfect! You don't need cutting-edge AI for recruiter responses.

## Using Paid APIs Instead (Optional)

If you prefer cloud APIs, you can use:

### OpenAI

```bash
# In env.example
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

### Anthropic Claude

```bash
# In env.example
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
```

But remember: **These cost money!** Ollama is free.

## Model Selection Guide

Choose based on your needs:

| Model | Size | RAM Needed | Use Case |
|-------|------|------------|----------|
| phi | 2.7GB | 4GB | Testing, simple responses |
| llama2:7b | 3.8GB | 8GB | **Recommended** - Good balance |
| mistral | 4.1GB | 8GB | Alternative to llama2 |
| llama2:13b | 7.4GB | 16GB | Better quality, slower |
| codellama | 3.8GB | 8GB | If recruiters send code challenges |

## Next Steps

1. Install Ollama
2. Pull llama2: `ollama pull llama2`
3. Verify it works: `ollama run llama2 "test"`
4. Update `env.example` if using a different model
5. Run the AI Recruiter Agent!

---

**Need help?** Visit [ollama.ai/docs](https://ollama.ai/docs)

