import pandas as pd
import viz_backup

art = pd.DataFrame({'nationality':['A', 'A', 'B', 'C'],
                   'gender':['M', 'M', 'F', 'M'],
                   'decade':['1930', '1940', '1930', '1940']})

print(art)

viz.make_sankey(art, 'nationality', 'gender', )