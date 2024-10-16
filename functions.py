import pandas as pd
import sqlite3
import plotly.graph_objs as go 
import numpy as np
import random




conn = sqlite3.connect('DataBase.db')
select = "SELECT * FROM team_scores_1"
df = pd.read_sql_query(select, conn)


### Anonymize ###
pseudo_names = ["Zorix", "Lumen", "Taris", "Sivel", "Nydra", "Voren", "Kaira", "Elvin", "Zaris",\
                "Relon", "Tirin", "Almen", "Oulen", "Bayl", "Nist", "Cloud", "Elmon"]
names = df["name"].unique().tolist()
random_pseudo_names = random.sample(pseudo_names, len(names))
anonymous_zip_dict = dict(zip(names, random_pseudo_names))
anonymous_names = [name for name in anonymous_zip_dict.values()]


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
        tw_global_mean = round(float(df['team_work'].mean()), 2)
        hs_global_mean = round(float(df['hard_skill'].mean()), 2)

        return tw_global_mean, hs_global_mean
    
    def global_mean_each_member(self):
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
    
    def last_mean(self):
        evaluations = self.last_survey()
        tw_data_last = []
        hs_data_last = []
        
        for name, item in evaluations.items():
            tw_data_last.append(item['team_work'])
            hs_data_last.append(item['hard_skill'])

        # Evitar división por 0
        if len(tw_data_last) > 0:
            tw_data_mean = round(sum(tw_data_last) / len(tw_data_last),2)
        else:
            tw_data_mean = 0
        
        if len(hs_data_last) > 0:
            hs_data_mean = round(sum(hs_data_last) / len(hs_data_last))
        else:
            hs_data_mean = 0

        return tw_data_mean, hs_data_mean

    def graph(self, evaluations, title, means):
        names = list(evaluations.keys())
        team_work = [evaluations[name]['team_work'] for name in names]
        hard_skill = [evaluations[name]['hard_skill'] for name in names]
        
        # Añadir "jitter" a los puntos para evitar la superposición completa
        jitter_strength = 0.09
        team_work_jittered = np.array(team_work) + np.random.uniform(-jitter_strength, jitter_strength, len(team_work))
        hard_skill_jittered = np.array(hard_skill) + np.random.uniform(-jitter_strength, jitter_strength, len(hard_skill))

        # Limita los valores dentro del rango [0, 10]
        team_work_jittered = np.clip(team_work_jittered, 0, 10)
        hard_skill_jittered = np.clip(hard_skill_jittered, 0, 10)


        fig = go.Figure()

        for i in range(len(anonymous_names)):
            fig.add_trace(go.Scatter(
                x=[round(team_work_jittered[i], 1)],
                y=[round(hard_skill_jittered[i], 1)],
                mode='markers+text',
                name=anonymous_names[i],  # leyenda
                text=[anonymous_names[i]],
                textposition='top center',
                textfont=dict(size=12),
                marker=dict(size=10)

            ))

        # Añadir las áreas de colores
        fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5,
                    fillcolor="red", opacity=0.1, line_width=0)
        fig.add_shape(type="rect", x0=0, y0=10, x1=5, y1=means[1],
                    fillcolor="yellow", opacity=0.1, line_width=0)
        fig.add_shape(type="rect", x0=10, y0=10, x1=means[0], y1=means[1],
                    fillcolor="green", opacity=0.1, line_width=0)
        fig.add_shape(type="line", x0=means[0], y0=0, x1=means[0], y1=10, 
                      line=dict(color="Red", width=2, dash="dash"))
        fig.add_shape(type="line", x0=0, y0=means[1], x1=10, y1=means[1], 
                      line=dict(color="Red", width=2, dash="dash"))

        # Configuración del layout del gráfico
        fig.update_layout(title=title,
                        xaxis_title="Team Work",
                        yaxis_title="Hard Skills",
                        xaxis=dict(range=[0, 10.3], dtick=1),
                        yaxis=dict(range=[0, 10.25], dtick=1),
                        showlegend=True)  # Esto asegura que la leyenda se muestre

        # Convertir el gráfico a HTML
        graph_html = fig.to_html(full_html=False)

        return graph_html
    
    # Funcion para anonimizar datos en formato {"pseudoname": [n, n2, n3, n4, ....]}
    def anon(self, option):
        evolution_anon = {}
        data = self.get_data(option)

        for real_name, evaluation_data in data.items():
            if real_name in anonymous_zip_dict:
                new_name = anonymous_zip_dict[real_name]
            else:
                new_name = "Doe"  
            evolution_anon[new_name] = evaluation_data

        return evolution_anon
    
    # Formato {"date": n, "date2": n2}
    def global_mean_date(self, option):
        global_mean_by_date = {}

        for date in self.dates:
            date_data = df[df['date'] == date]
            tw_mean_by_date = date_data[option].mean()
            global_mean_by_date[date] = round(float(tw_mean_by_date), 2)

        return global_mean_by_date


    # Graph para evolucion de team_work
    def tw_evolution(self):
        
        tw_evolution_data = self.global_mean_date(option="team_work")

        fig = go.Figure()

        # Convertir fechas y puntuaciones en listas para pasarlas a go.Scatter
        dates = list(tw_evolution_data.keys())
        scores = list(tw_evolution_data.values())

        fig.add_trace(go.Scatter(x=dates, y=scores, mode='lines+markers'))

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
        hs_evolution_data = self.global_mean_date(option="hard_skill")
        
        fig = go.Figure()

        dates = list(hs_evolution_data.keys())
        scores = list(hs_evolution_data.values())
        
        fig.add_trace(go.Scatter(x=dates, y=scores, mode='lines+markers'))

        fig.update_layout(
            title="Hard-Skills Evolution",
            xaxis_title="Date",
            yaxis_title="Hard-Skills",
            xaxis=dict(tickvals=self.dates),
            yaxis=dict(range=[0, 10.5], dtick=1)
        )

        hs_graph_html = fig.to_html(full_html=False)

        return hs_graph_html


    


if __name__ == '__main__':
    sep = SepTeam()
    data = sep.get_data('team_work')
    print(data)