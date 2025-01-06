# TP Big Data - Gr 11

---

BRUZEAU Jules

ESSLIMANI Younes

DETREZ Mathias

---

> Toutes les données utilisées pour ce projet proviennent de l’API officiel de Riot Games:
https://developer.riotgames.com/apis
> 

# Problématique et objectifs

## Problématique

<aside>
💡 **Comment les tendances stratégiques et la méta évoluent-elles dans League of Legends, et quels impacts ces évolutions ont-elles sur les performances des joueurs et des champions ?**

</aside>

League of Legends est un jeu en constante évolution, où les mises à jour régulières modifient les règles, ajustent les caractéristiques des champions et introduisent des nouveautés. Ces changements influencent directement :

1. Les choix stratégiques des joueurs, comme les champions et rôles privilégiés.
2. La métagame ****(méta), définie comme l’ensemble des stratégies perçues comme les plus efficaces à un moment donné.

Cette problématique explore l’impact de ces changements sur :

- Les champions joués et leurs taux de victoire.
- Les performances des joueurs selon leurs rôles.
- La durée des parties et les objectifs atteints (dragons, tours détruites, etc.).

## Objectifs

L’objectif principal est de comprendre l’évolution des stratégies et de la méta dans League of Legends en s’appuyant sur des données de jeu collectées via l’API de Riot Games. Cela inclut :

1. Identifier les tendances stratégiques dans les choix de champions :
    - Quels champions sont les plus joués après une mise à jour ?
    - Quels rôles ont le plus d’impact sur le résultat d’une partie ?
    - Les changements dans les taux de victoire des champions en fonction des patches.
2. Analyser les effets des mises à jour :
    - Impact des ajustements (buffs, nerfs) sur les performances des champions.
    - Changement dans la répartition des rôles joués.
3. Comprendre les indicateurs clés de performance (KPIs) dans le cadre de la méta :
    - Corrélation entre les choix de champions et les résultats (victoires/défaites).
    - Évolution des temps moyens de parties par patch.
    - Objectifs atteints (tours, dragons, barons) et leur influence sur la méta.

# Données & Dataset

> Toutes les données utilisées pour ce projet proviennent de la source suivante:
https://developer.riotgames.com/apis
> 

Pour répondre à la problématique, voici les données nécessaires et les indicateurs associés:

1. **Données des matchs** (Match API)
2. **Données des champions** (Champion API)
3. **Données des joueurs** (Summoner API)

## Collecte des données (Zone Bronze)

### Définition des endpoints nécessaires

L’objectif est de récupérer les données brutes relatif aux indicateurs présenté ci-dessus à partir de l’API de Riot Games et les organiser dans une structure de stockage.

Voici la liste des routes utilisées pour la collecte des données.

| API | URL | Description |
| --- | --- | --- |
| Global | https://ddragon.leagueoflegends.com/api/versions.json | Récupérer la liste des versions du jeux. |
| Global | https://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json | Récupérer les champions et leur données d’une version du jeux. |
| Summoner | {baseUrl}/lol/league/v4/challengerleagues/by-queue/{queue} | Récupérer le classement actuel d’une league par région. |
| Summoner | {baseUrl}/lol/summoner/v4/summoners/{summonerId} | Récupérer les informations sur un joueur. |
| Match | {baseUrl}/lol/match/v5/matches/by-puuid/{puuid}/ids | Récupérer une liste d’Id de matchs pour un joueur. |
| Match | {baseUrl}/lol/match/v5/matches/{matchId} | Récupérer le détails et toutes les données d’un match. |

### Récupération des données nécessaires

Pour répondre au mieux à notre problématique et constituer un jeu de donnée suffisamment conséquent, nous avons choisis de récupérer de la donnée sur trois régions du jeu, l’Europe, la Corée du Sud et le Japon.

Pour chacune de ces régions, nous avons récupérer les 50 derniers matches des 100 meilleurs joueurs actuel de ces région dans le mode classé traditionnel (5v5).

Nous avons ensuite créer nos script Python pour récupérer les données nécessaires et les stockers à l’intérieur de fichier JSON (format de donnée renvoyer par l’API).

Vous pouvez trouver l’ensemble des scripts utilisé sur ce [repository](https://github.com/JulesEfrei/big-data-efrei-m1).

### Organisation des données brutes

Pour stocker nos données, nous avons choisis la structure de fichier suivante:

```bash
/data/	
   /bronze/
	   champions.json
	   players.json
	   matches.json
	 /silver/
		 ...
	 /gold/
		 ...
```

## Nettoyage des données (Zone silver)

Voici la table de rejet créer pour ce projet:

| Id | Table | Rejet |
| --- | --- | --- |
| 1000 | champions | Nom du champion manquant |
| 1001 | champions | Id du champion manquant |
| 1002 | champions | Tags manquant |
| 1003 | champions | Attaque invalide |
| 1004 | champions | Défense invalide |
| 1005 | champions | Difficulté manquante |
| 2000 | players | PUUID manquant |
| 2001 | players | SummonerId manquant |
| 2002 | players | Région manquante |
| 2003 | players | LeaguePoints invalide |
| 3000 | matches | Ligne dupliqué |
| 3001 | matches | Champs manquant |
| 3002 | matches | Type invalide |
| 3003 | matches | Valeur aberrante |

Pour chaque table de la zone bronze (players, champions, matches), nous avons créer une nouvelle table dans la zone silver en sélectionnant, typant et nettoyant tous les champs avec l’aide de la table de rejet. Les données rejetées sont insérer dans la table de rejet correspondante (champions_rejected, players_rejected et matches_rejected) 

## Modélisation du DataWarehouse (Zone Gold)

### Table de faits

Voici la structure de notre table de fait, `gold.matches_fact`:

- gameId → long
- summonerId → string
- champion_id → long
- champion_name → string
- teamId → long
- year → integer
- month → integer
- day → integer
- hour → integer
- day_of_week → integer
- total_kills → long
- total_deaths → long
- total_assists → long
- total_damage_dealt → long
- total_damage_taken → long
- team_win → integer
- total_baron_kills → long
- total_dragon_kills → long
- total_tower_kills →long
- total_riftHerald_kills → long
- total_inhibitor_kills →long

### Dimensions

Structure de la dimension `gold.champions_dimension`:

- champion_id → long
- champion_name → string
- attack → integer
- defense → integer
- difficulty → integer
- magic → integer
- impact_score → integer
- is_tank → boolean
- is_assassin → boolean
- hp → float
- attack_damage → float
- armor → float

Structure de la dimension `gold.player_dimension`:

- puuid → string
- summonerId → string
- region → string
- rank → string
- leaguePoints → integer
- wins → integer
- losses → integer
- freshBlood → boolean
- hotStreak → boolean
- inactive → boolean
- veteran → boolean
- win_rate → double
- league_points_per_win → double

Structure de la dimension `gold.time_dimension`:

- gameId → long
- game_start_date → date
- year → integer
- month → integer
- day → integer
- hour → integer
- day_of_week → integer

Structure de la dimension `gold.teams_dimension`:

- gameId → long
- teamId → long
- baron_kills → long
- dragon_kills → long
- tower_kills → long
- riftHerald_kills → long
- inhibitor_kills → long
- team_win → integer

# Visualisation des données

Voir `notebooks/rapport`.

# Fetch fresh data

```bash
docker build -t riot-api-fetcher .
./fetch.sh <champions | players | matches>
```
