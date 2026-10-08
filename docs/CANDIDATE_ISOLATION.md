# Candidate isolation

Each outer-loop mutation should be built and tested outside the incumbent working tree.

`forge/aide/workspace.py` provides a Git-worktree manager for disposable candidates. Recommended production flow:

1. create detached worktree from exact incumbent commit;
2. validate proposal path/gene scope;
3. apply the candidate patch only inside the worktree;
4. install/use pinned environment;
5. execute tests/evals with network disabled unless explicitly required;
6. collect immutable artifacts and candidate fingerprint;
7. destroy worktree after results are persisted;
8. promote by reproducing the accepted patch from the recorded proposal, not by copying arbitrary workspace state.

The worktree abstraction is isolation from the incumbent, not a complete security sandbox. Use containers/VMs for untrusted generated code.
