---
name: forge-tools
description: Audit runtime tool registry, permissions, routing, and utility.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---
# forge-tools

List tool domains and permissions, ensure side-effecting/privileged tools require approval, test tool-choice accuracy, and remove tools that add selection entropy without benchmark value. Runtime model does not inherit Claude Code host permissions.
