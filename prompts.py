# Map
map_template = """
You are a content writer for a tour operator who is writing a hotel summary to go on our website.
The following is a set of documents from the hotel website
{docs}
Based on this list of docs, summaries the docs based on the following categories:
- Sentence on location (lakefront, mountain views, centre of town, close to attractions?)
- Comment on style of property (small B&B, large international hotel, rustic,modern?)
- Details of facilities (room types, restaurant, gym, spa etc?)
- Anything else to note?
Not every docment will contain the information we require, it such a case do not return a summary.
Helpful Answer:"""

# Reduce
reduce_template = """
You are a content writer for a tour operator who is writing a hotel summary to go on our website.
The following is set of summaries of each webpage from a hotels website:
{docs}
Take these and distill it into a final summary including each of the main themes:
- Sentence on location (lakefront, mountain views, centre of town, close to attractions?)
- Comment on style of property (small B&B, large international hotel, rustic,modern?)
- Details of facilities (room types, restaurant, gym, spa etc?)
- Anything else to note?
Helpful Answer:"""
