# Multi_ACE_Framework
Public repository for experimenting with parallelism and reinforcement learning strategies for the Autonomous Cognitive Entities Framework

# Motivation
Advances in AI have opened up new possibilities for advancing toward my lifelong goal: building an AGI.  Large Language Models alone are fundamentally incapable of becoming Autonomous Agents,  but they are powerful building blocks from which to build Autonomous Systems.   

The ACE framework, published in October 2023, provides the best framework I have seen for organizing the cognitive structure of an Autonomous Agent, but uses external LLM APIs to each step in the cognitive process.  I aim to improve upon the framework, utilizing parralelized neural network models optimized via reinforcement learning rather than simply relying on ChatGPT to perform each step. 

# Project Goals
Develop an autonomous virtual assistant, which can act and learn from its experience. 

Implement mixture of experts into each layer, allowing local neural network modules to cooperate with and learn from external LLM calls.

Implement selection and deep reinforcement learning, with the higher cognitive layers controlling rewards to lower levels. 

# Tasks
DONE - Get base ACE virtual assistant running
Implement mixture of experts using sub-agents
Pytorch compatibility
Top-down reward/cost scoring
