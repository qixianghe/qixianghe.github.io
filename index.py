import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact, interactive
import numpy as np


link = "https://github.com/qixianghe/SPLTeams/raw/master/SPL-2016-2020.csv"

masterdf = pd.read_csv(link, index_col=None)

masterdf = masterdf.drop(labels = 'Unnamed: 0', axis=1)

# Get a list of the columns we want to examine
columnslist = list(masterdf.columns)
selectedcolumnslist = columnslist[columnslist.index('AVERAGE INSTAT INDEX'):columnslist.index('YEAR')]
# print(selectedcolumnslist)

# List of teams now 
teamslist = list(set(masterdf['TEAM']))

# List of years now
yearslist = list(set(masterdf['YEAR']))

yearslist.sort()

# List of the years
xlist = [int(x) for x in yearslist]
# print(xlist)

def updategraph(team1, team2, team3, matchaction):

  selectedteams = [team1, team2, team3]
  holdingdict = {}
  holdinglist = []
  for year in yearslist:
    holdingdict[year] = {}

    for team in selectedteams:
      tempdf = masterdf[(masterdf['YEAR'] == year) & (masterdf['TEAM'] == team)]
      meanvalue = tempdf[matchaction].mean()
      holdingdict[year][team] = meanvalue
      holdinglist.append([team,year,meanvalue])

    # tempdf = masterdf[(masterdf['YEAR'] == years) & (masterdf['TEAM'] == team)]
    # meanvalue = tempdf[matchaction].mean()
    # yvalues.append(meanvalue)

  refdf = pd.DataFrame(holdinglist, columns = ['team','year','value'])

  # fig = go.FigureWidget()
  fig = px.bar(refdf, x='year', y = 'value', color='team',
               title = f"Average {matchaction} per match for each season",
                width = 1200, height = 600)
  
  fig.update_yaxes(title=matchaction)
  fig.update_xaxes(title='Season')
  
  fig.update_layout(barmode = 'group')
  
  # Calculate the mean value across whole league for selected match action
  totalmeanvalue = masterdf[matchaction].mean()

  # fig.add_shape(type='line', 
  #             xref="x", yref="y",
  #             x0=2015.5, y0=totalmeanvalue, x1=2020.5, y1=totalmeanvalue,
  #             line=dict(
  #                 color = "Orange",
  #                 width = 3,
  #                 dash = "dot"),
  #             text = ['TESTING HERE'])
  

  
  fig.add_trace(go.Scatter(x=[2015.5,2020.5], y = [totalmeanvalue,totalmeanvalue],
                    mode='lines',
                    name='League average',
                    text='League average',
                    textposition='top right',
                    line=dict(
                    color = "Orange",
                    width = 3,
                    dash = "dot")
                    ))
  


  z = np.polyfit(xlist, yvalues, 1)
  p = np.poly1d(z)
  trendliney = p(xlist)

  # fig.add_trace(xlist, y)

  # fig.add_shape(type='line', 
  #               xref="x", yref="y",
  #               x0=2016, y0=trendliney[0], x1=2020, y1=trendliney[-1],
  #               line=dict(
  #                   color = "Orange",
  #                   width = 3,
  #                   dash = "dot"
  #               ))

  # fig.add_annotation(title='TESTING')

  fig.show()


widget = interactive(updategraph, team1 = teamslist, team2 = teamslist, team3 = teamslist, matchaction = selectedcolumnslist)
container = widgets.HBox(widget.children[:-1])
output = widget.children[-1]

display(widgets.VBox([container, output]))

# interactive(updategraph, team1 = teamslist, team2 = teamslist, team3 = teamslist, matchaction = selectedcolumnslist)
