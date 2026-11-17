task_solve_with_insights = """
## Here are some successful examples similar to the current problem:
{few_shots}

## Here are some successful execution processes you have carried out in tasks similar to the current one.
Please carefully refer to their execution process, especially when you encounter difficulties:
{memory_few_shots}

(END OF EXAMPLES)

## The following are some experience you gather on a similar task of completing a household task by interacting in a household environment.
** Use these as references to help you perform this task and avoid unnecessory thinking**:
{insights}

## Now it's your turn!
{task_description}
"""

task_format: str = """
### Task description:   
{task_description}    

### Key steps:
{key_steps}

### Detailed trajectory:
{trajectory}
"""

temp = """NOTE: You must use the command `think: <your thoughts here>` if you want to think!!!
    - Right output: think: To solve the task, ...
    - Wrong output: To solve the task, ... """

def format_task_prompt_with_insights(
    few_shots: list[str],
    memory_few_shots: list[str],
    insights: list[str],
    task_description: str 
) -> str: 
    
    existing_rules_text: str = '\n'.join([f'{i}. {r}' for i, r in enumerate(insights, 1)])
    memory_few_shots: str = '\n\n'.join([f"Task {i+1}:\n{shot}" for i, shot in enumerate(memory_few_shots)])
    user_prompt: str = task_solve_with_insights.format(
        few_shots='\n'.join(few_shots),
        memory_few_shots=memory_few_shots,
        task_description=task_description,   
        insights=existing_rules_text,
    )

    return user_prompt

def format_task_context(task_description: str, task_traj: str, key_steps: str = None) -> str:

    return task_format.format(
        task_description=task_description,
        key_steps=key_steps,
        trajectory=task_traj
    )