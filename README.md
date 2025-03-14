# Project-3

## Questions:

1. **Discipline-Specific Insights:**
   - Are there specific fields where open access publishing is more prevalent among female authors compared to male authors, or vice versa?
   - How do gender representation and open access adoption vary across STEM fields compared to humanities and social sciences?

2. **Temporal Changes:**
   - How has gender representation in open access publishing evolved over the past decade?
   - Are there any significant shifts in gender representation in open access publishing during major global events (e.g., pandemic)?
  
3. **Collaborative Patterns:**
   - Is there a difference in the collaboration patterns (e.g., co-authorship networks) between genders in open access versus traditional publishing models?
   - How do collaborative efforts in open access journals differ by gender and discipline?

## Sources:
- https://api.openalex.org/
  
## Views/visualizations:
1. For temporal changes, use a line chart to show the trend of open access publishing by gender over time, highlighting significant events and shifts.
2. For discipline-specific insights, use a bar chart to compare the percentage of open access publications.
3. For collaborative patterns, use a network graph to visualize co-authorship networks, differentiating between genders.


## Workflow:
### Extract, Transform, Load (ETL) process for the OpenAlex API data
- Extract:
- - In python, use requests library to call the openAlex API to get a random author
- - Use the author ID to get the author's publications
- - For each publication, get the authors. Store these as 'collaborators'.
- Transform: 
- - Clean the data:
- - - Remove duplicates
- - - Remove irrelevant fields (requires thought)
- - - Standardize author names and publication titles
- - - Convert publication dates to a standard format
- - - Handle missing values (e.g., fill in with 'unknown' or 'not available')
- - Perform normalization on the data:
- - - 1NF: make sure no field is multi-valued 
- - - 2NF: ensure all non-key attributes are fully functional dependent on the primary key
- - - 3NF: remove transitive dependencies
- Load:
- - Load the cleaned data into a postgreSQL database using SQLAlchemy:
- - - Export this database to sqlite for use in the web app

### User Interface
- - Three webpages, one for each question.
- - - Temporal changes: line chart (static) (static)
- - - Discipline-specific insights: bar chart/pie chart  (static)
- - - Collaborative patterns: network graph (dynamic)
- - - - User can input an author's name and see their co-authorship network:
- - - - - - node size = number of collaborations with root author
- - - - - - edge size = number of collaborations between two authors
- - - - - - color = gender
- - - - User can set max distance from root author in the network
- - - - User can toggle visibility of collaborations (e.g., by gender or publication year)
- - - - (Ambitious) User can click on a node to set it as the new root author and see their co-authorship network 
- - - - - (OR) User can click on a node to see the author's profile and publications in a new tab
- - - - - (OR) User can click on a node to see the author's profile and publications in a modal
- - - - - (OR) User can click on a node to see the author's profile and publications in a tooltip
- - - - - (OR) User can click on a node to see the author's profile and publications in a sidebar