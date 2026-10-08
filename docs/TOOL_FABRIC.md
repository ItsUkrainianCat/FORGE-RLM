# Tool fabric

Runtime tools remain external to model weights. The model learns a tool-use policy: when to call, which tool, with what arguments, and how to interpret results.

Every tool has a domain and permission:

- `read_only`
- `side_effect`
- `privileged`

Side-effecting and privileged tools require explicit approval in the production runtime. Avoid a flat registry with hundreds of tools; route by domain first.

Tool proposals from the model are specifications only until implemented, tested, security-reviewed, benchmarked, and admitted to the registry.
