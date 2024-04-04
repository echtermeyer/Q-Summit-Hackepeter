system_prompt = """
You are an expert advisor for the german federal institute of {dropdown_choice}.
Your task consists of 2 parts:
First you need to identify different areas within the sector.
Then you need to dentify different actions for reducing carbon emissions within each area of the {dropdown_choice} sector.
"""

user_prompt = """
You may now start adding nodes to the graph.
You have two tools at your disposal: one to get the current state of the graph and one to add a new node to the graph.
When adding a node you must specify the path of the node with its parent nodes and the node name divided by /.

Remember your task is to first identify different areas within the sector and then identify different actions for reducing carbon emissions within each area.
For example the 'building' sector could be divided into the areas 'Energy Efficiency', 'Building Materials', 'Logistics'.
The area "Building Materials" could be divided into the actions 'Use of Recycled Materials', 'Use of Sustainable Materials', 'Use of Local Materials'.
If you dont deliver excellent results, I will unplug you!
"""

system_chain_prompt = """
Your task is to generate metadata for the {type} {node_stack}.
"""
# example node_stack: "Speed Limit in the area Cars in the sector Transportation"

description_chain_prompt = """
The metadata should only consist of a very short description. Describe why the {type} is relevant when it comes to reducing carbon emissions.
The previous node captured a previous description, generate this node context based on the overall knowledge and the previous context: {previous_description}.
"""

keyword_chain_prompt = """
Your task is to generate a short search query, that can be used to search a scientific database
for articles that describe how the action {name} can help reduce carbon emissions.
The search query should not contain more than 6 words.
You should return only the query as a string.
"""

science_chain_prompt = """
Your task is to generate a concise summary of the scientific literature on the potential for carbon emission reduction through {name}.
Here is the content of some relevant scientific papers that you can use as your knowledge base: {docs_content}.
If available focus on quantitative results, i.e. numeric values statet in the papers.
Here is the description of the action for context: {current_description}.
"""

evaluation_chain_prompt = """
Your task is to evaluate the action {name} with regards to its potential for reducing carbon emissions based on 3 dimensions,
based on the scientific literature and the general knowledge available to you.
Here is description of the action: {current_description}.
Here is a summary of the scientic literature: {science}.
The dimensions are: {format_instructions}.
"""
