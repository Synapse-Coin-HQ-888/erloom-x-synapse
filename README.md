
         ╭────────────────────────────────────────────────────────────╮                                                                                                                               
         │  ▄▄▄▄▄▄  ▄▄▄▄▄▄  ▄▄▄▄▄▄  ▄       ▄▄▄▄▄▄  ▄▄▄▄▄▄  ▄▄   ▄▄   │                                                                                                                               
         │  ██████  ██  ██  ██  ██  ██      ██  ██  ██  ██  ███▄▄███  │                                                                                                                               
         │  ██████  ██████  ██████  ██      ██  ██  ██  ██  ████████  │                                                                                                                               
         │  ██▄▄▄▄  ██▄▄██  ██▄▄██  ██      ██  ██  ██  ██  ██▄██▄██  │                                                                                                                               
         │  ██████  ██  ██  ██  ██  ██████  ██████  ██████  ██▄▄▄▄██  │                                                                                                                               
         ╰────────────────────────────────────────────────────────────╯   

         To construct an intelligence fractal decompression engine...
INFO
INFO     ──────────────────────────────────── Home Screen ────────────────────────────────────────
INFO
INFO     No .syn files found in prompts/ or syn/ directories
INFO
INFO     Basic Usage:
INFO       uv run main <synapseware> <command>
INFO       uv run main <loom_class> <command>
INFO
INFO     Commands:
INFO       dry     # Execute rollouts without training (uses MockClient by default)
INFO       train   # Perform full training with rollouts and optimization
INFO       dump    # Generate and save rollouts to the project directory
INFO       cat     # Display synapseware code or loom class source
INFO
INFO     Positional Arguments:
INFO       synapseware   # .syn file or shorthand (qa, tool, codemath, doublecheck, smola)
INFO       loom_class    # Loom class name for direct loom interaction
INFO       command       # One of: dry, train, dump
INFO       n             # Number of dataset rows to process (default: 10 for train, 1 for dry/dump)
INFO
INFO     Quick Examples:
INFO       uv run main qa.syn dry                              # Quick dry run with 1 sample
INFO       uv run main tool.syn train 50                       # Train with 50 samples
INFO       uv run main codemath.syn dry 5 --debug              # Debug dry run with 5 samples
INFO       uv run main smola.syn dump 3                        # Generate and save 3 rollouts
INFO       uv run main qa.syn cat                              # Display synapseware code
INFO       uv run main SynapsewareLoom cat                     # Display loom class source
INFO
INFO     Testing Examples:
INFO       uv run main prompt.syn train 1 --micro-test         # Minimal test mode
INFO       uv run main prompt.syn train 2 --local-test         # Local test mode
INFO       uv run main prompt.syn train 1 --cpu --test-steps 2 # CPU debug mode
INFO       uv run main compressor.syn train 1 --cpu --dry      # Dry training mode (no backprop)
INFO
INFO     Advanced Examples:
INFO       uv run main qa.syn train 100 --vllm --batch 16      # Distributed training
INFO       uv run main custom_loom train 50 --model llama-7b   # Custom loom with specific model
INFO       uv run main tool.syn train 200 --data custom_dataset # Training with custom dataset
INFO
INFO     Client Options:
INFO       --vllm         # Use VLLM for distributed training
INFO       --openai       # Use OpenAI API (requires OPENAI_API_KEY)
INFO       --openrouter   # Use OpenRouter API (requires OPENROUTER_API_KEY)
INFO       --lmstudio     # Use LM Studio local server
INFO       --client URL   # Custom OpenAI-compatible endpoint
INFO
INFO     Testing & Debug Options:
INFO       --cpu          # Run on CPU (slower but unlimited memory)
INFO       --micro-test   # Minimal memory usage for testing
INFO       --local-test   # Optimized for local development
INFO       --test-steps N # Limit training to N steps
INFO       --debug        # Enable detailed debug logging
INFO       --unsafe       # Disable safe mode (raises errors immediately)
INFO
INFO     Deployment:
INFO       uv run main --vastai                               # Deploy to VastAI
INFO       uv run main --vastai-gui                           # Launch VastAI deployment GUI
INFO
INFO     Use uv run main <command> --help for detailed options.
INFO
INFO     ─────────────────────────────────────────────────────────────────────────────────────────
