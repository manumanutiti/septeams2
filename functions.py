import pandas as pd
import sqlite3
import plotly.graph_objs as go 
import numpy as np



conn = sqlite3.connect('DataBase.db')
select = "SELECT * FROM team_scores_1"
df = pd.read_sql_query(select, conn)


class SepTeam:
    def __init__(self):
        self.names = df["name"].unique().tolist()
        dates_unprocessed = df['date'].unique()
        self.dates = [date for date in dates_unprocessed]

    def get_data(self, option):
        evaluation_data = {}
        for name in self.names:
            name_evolution = df[df['name'] == name][option].to_list()
            evaluation_data[name] = name_evolution
        return evaluation_data
    
    def global_mean(self):
        evaluations = {}
        for name in self.names:
            team_member = df[df['name'] == name]
            team_member_tw_mean = team_member['team_work'].mean()
            team_member_hs_mean = team_member['hard_skill'].mean()

            evaluations[name] = {
                'team_work': float(team_member_tw_mean),
                'hard_skill': float(team_member_hs_mean)
            }

        return evaluations
    
    def last_survey(self):
        evaluations = {}
        last = df["date"].max()
        last_survey = df[df["date"] == last]
        
        for name in self.names:
            team_member = last_survey[last_survey['name'] == name]
            
            if not team_member.empty:
                team_member_tw = team_member['team_work'].values[0]
                team_member_hs = team_member['hard_skill'].values[0]
            else:
                team_member_tw = None
                team_member_hs = None

            # Solo guardar si ambos valores no son None
            if team_member_tw is not None and team_member_hs is not None:
                evaluations[name] = {
                    'team_work': int(team_member_tw),
                    'hard_skill': int(team_member_hs)
                }

        return evaluations


    def graph(self, evaluations, title):
        names = list(evaluations.keys())
        team_work = [evaluations[name]['team_work'] for name in names]
        hard_skill = [evaluations[name]['hard_skill'] for name in names]
        
        # Añadir "jitter" a los puntos para evitar la superposición completa
        jitter_strength = 0.09
        team_work_jittered = np.array(team_work) + np.random.uniform(-jitter_strength, jitter_strength, len(team_work))
        hard_skill_jittered = np.array(hard_skill) + np.random.uniform(-jitter_strength, jitter_strength, len(hard_skill))

        fig = go.Figure()

        for i in range(len(names)):
            fig.add_trace(go.Scatter(
                x=[round(team_work_jittered[i], 1)],
                y=[round(hard_skill_jittered[i], 1)],
                mode='markers+text',
                name=names[i],  # leyenda
                text=[names[i]],
                textposition='top center',
                textfont=dict(size=10),
                marker=dict(size=10)

            ))

        # Añadir las áreas de colores
        fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5,
                    fillcolor="red", opacity=0.1, line_width=0)
        fig.add_shape(type="rect", x0=0, y0=10, x1=5, y1=5,
                    fillcolor="yellow", opacity=0.1, line_width=0)
        fig.add_shape(type="rect", x0=10, y0=10, x1=5, y1=5,
                    fillcolor="green", opacity=0.1, line_width=0)

        # Configuración del layout del gráfico
        fig.update_layout(title=title,
                        xaxis_title="Team Work",
                        yaxis_title="Hard Skills",
                        xaxis=dict(range=[0, 10.5], dtick=1),
                        yaxis=dict(range=[0, 10.5], dtick=1),
                        showlegend=True)  # Esto asegura que la leyenda se muestre

        # Convertir el gráfico a HTML
        graph_html = fig.to_html(full_html=False)

        return graph_html
    
    # Graph para evolucion de team_work
    def tw_evolution(self):
        tw_evolution = self.get_data('team_work')
        fig = go.Figure()

        for name, scores in tw_evolution.items():
            fig.add_trace(go.Scatter(x=self.dates, y=scores, mode='lines+markers', name=name))

        fig.update_layout(
            title="TeamWork Evolution",
            xaxis_title="Date",
            yaxis_title="Team-work",
            xaxis=dict(tickvals=self.dates),
            yaxis=dict(range=[0, 10.5], dtick=1)
        )

        tw_graph_html = fig.to_html(full_html=False)

        return tw_graph_html
    
    # Grafico para hard_skill evolution

    def hs_evolution(self):
        hs_evolution_data = self.get_data('hard_skill')
        fig = go.Figure()

        for name, scores in hs_evolution_data.items():
            fig.add_trace(go.Scatter(x=self.dates, y=scores, mode='lines+markers', name=name))
        
        fig.update_layout(
            title="Hard-Skills Evolution",
            xaxis_title="Date",
            yaxis_title="Hard-Skills",
            xaxis=dict(tickvals=self.dates),
            yaxis=dict(range=[0, 10.5], dtick=1)
        )

        hs_graph_html = fig.to_html(full_html=False)

        return hs_graph_html
    
    def global_info(self):
        pass

    


