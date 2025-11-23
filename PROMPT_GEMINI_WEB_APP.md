# Prompt pour Gemini 3 - Web App Vitalist

## Contexte du Projet

Tu es un développeur expert chargé de créer une **application web interactive complète** pour le projet **Vitalist**, un système d'analyse du vieillissement différentiel des organes basé sur les données NHANES.

### Vue d'ensemble du projet Vitalist

Vitalist est un projet de data science qui utilise le machine learning pour analyser le vieillissement au niveau des organes individuels. Le concept clé :

- **Organ Clocks** : Modèles ML qui prédisent l'âge chronologique à partir de biomarqueurs spécifiques à chaque organe
- **Biological Age** : L'âge prédit par le modèle pour un organe donné
- **Age Gap** : Différence entre l'âge biologique et l'âge chronologique (positif = vieillissement accéléré)
- **5 systèmes d'organes analysés** :
  - **Liver** (Foie) : ALT, AST, GGT, albumine, bilirubine
  - **Kidney** (Rein) : Créatinine, BUN, acide urique, ratio albumine/créatinine
  - **Cardio-Metabolic** : Tension artérielle, cholestérol, triglycérides, glucose, HbA1c, BMI
  - **Immune** (Immunitaire) : Globules blancs, lymphocytes, neutrophiles, monocytes
  - **Hematologic** (Hématologique) : Globules rouges, hémoglobine, hématocrite, plaquettes

### Le besoin

Le projet actuel est structuré autour de **7 notebooks Jupyter** (00 à 06), avec le notebook 06 servant de "rapport narratif" pour un jury. Nous voulons créer une **application web professionnelle et autonome** qui :

1. **Remplace le notebook 06** avec une interface moderne et interactive
2. **Intègre tous les outputs** du projet (données, métriques, visualisations)
3. **Se suffit à elle-même** : l'application doit être autonome et déployable
4. **Utilise une approche Static Data Export** pour maximiser les performances

---

## Architecture Technique Requise

### Stack Technique Obligatoire

**Frontend :**
- **Framework moderne** : React avec TypeScript ou Next.js (recommandé pour SSG)
- **Styling** : Tailwind CSS + shadcn/ui (ou équivalent : Material-UI, Chakra UI)
- **Charting/Visualisation** :
  - Recharts ou Chart.js pour les graphiques standards
  - D3.js pour les visualisations complexes (heatmaps, profils individuels)
  - Plotly.js si besoin d'interactivité avancée
- **State Management** : Context API ou Zustand (léger)

**Approche Static Data Export (CRITIQUE) :**
- **Pré-génération des données** : Les données doivent être exportées depuis les notebooks Python vers des fichiers JSON/CSV statiques
- **Pas de backend en temps réel** : L'application doit fonctionner avec des données statiques pré-calculées
- **Structure des exports** :
  ```
  web_app/public/data/
  ├── age_gaps.json          # Données complètes des age gaps
  ├── metrics_summary.json   # Métriques des modèles
  ├── correlations.json      # Matrice de corrélation
  ├── trajectories.json      # Données des trajectoires pseudo-longitudinales
  ├── clusters.json          # Résultats du clustering
  ├── individuals/           # Profils individuels
  │   └── {seqn}.json       # Un fichier par individu
  └── feature_importance/    # Importance des features
      ├── liver.json
      ├── kidney.json
      └── ...
  ```

**Build & Deploy :**
- Static Site Generation (SSG) avec Next.js ou équivalent
- Déployable sur Vercel, Netlify, ou GitHub Pages
- Aucune dépendance serveur nécessaire

---

## Structure de l'Application Web

### Pages/Sections Principales

L'application doit avoir une structure claire avec navigation :

#### 1. **Page d'Accueil / Executive Summary**
- **Hero Section** :
  - Titre principal : "Vitalist - Organ-Specific Aging Analysis"
  - Sous-titre expliquant le concept des organ clocks
  - Statistiques clés en grands chiffres :
    - Nombre d'individus analysés : 531
    - Nombre d'organes étudiés : 5
    - Pourcentage avec vieillissement accéléré multi-organes
- **Key Findings** : 4-6 points principaux avec icônes
- **Navigation visuelle** vers les sections principales

#### 2. **Methodology & Data**
- **Section "The Problem"** :
  - Explication : Chronological age ≠ Biological age
  - Concept des organ clocks illustré
  - Définition de l'Age Gap
- **Data Source : NHANES** :
  - Présentation de NHANES
  - Limitation : données cross-sectionnelles (pas longitudinales)
  - Tableau des 5 organes avec leurs biomarqueurs
- **Pipeline Methodology** :
  - Diagramme visuel du pipeline (Data Prep → Feature Engineering → Training → Analysis)
  - Technologies utilisées (ElasticNet, HistGradientBoosting)

#### 3. **Model Performance**
- **Tableau comparatif** :
  - Colonnes : Organ | Linear MAE | NonLinear MAE | Improvement | R²
  - Données depuis `metrics_summary.json`
  - Tri et filtres interactifs
- **Graphiques de comparaison** :
  - Bar chart : Linear vs Non-Linear MAE par organe
  - Scatter plot : R² train vs test pour détecter l'overfitting
- **Key Insights** :
  - "Non-linear models outperform linear by 18-27%"
  - "Cardio-metabolic system shows best predictive performance"

#### 4. **Age Gap Analysis** (Section principale)

**4.1 Distributions**
- **Histogrammes/Violin plots** pour chaque organe :
  - Distribution des age gaps
  - Overlay d'une ligne à 0 (âge chronologique)
  - Zones colorées : gap > +5 (accéléré), gap < -5 (ralenti)
- **Summary statistics** : Mean, Std, Min, Max pour chaque organe
- **Filtres interactifs** :
  - Sélection d'organes à afficher
  - Filtres par âge, sexe si disponible

**4.2 Inter-Organ Correlations**
- **Heatmap interactive** :
  - Matrice de corrélation entre les age gaps des 5 organes
  - Tooltip avec valeurs exactes au hover
  - Gradient de couleurs (bleu négatif, rouge positif)
- **Insights clés** :
  - "Cardio-metabolic and kidney aging often co-occur"
  - "Some organs age independently"

**4.3 Accelerated Aging Patterns**
- **Bar chart** : Distribution du nombre d'organes en vieillissement accéléré par individu
- **Statistiques** :
  - % avec au moins 1 organe accéléré
  - % avec multi-organe accéléré (>1)
- **Risk stratification** : Identification des individus à haut risque

**4.4 Pseudo-Longitudinal Trajectories**
- **Line chart** : Évolution moyenne des age gaps par tranche d'âge
  - 5 lignes (une par organe)
  - Tranches : 18-30, 30-40, 40-50, 50-60, 60-70, 70-80
  - Mise en évidence des organes qui "cassent" en premier
- **Warning** : "Cross-sectional data, not true longitudinal tracking"

#### 5. **Aging Phenotypes** (Clustering)
- **Scatter plot 2D** : Projection UMAP/PCA des profils de vieillissement
  - Points colorés par cluster
  - Tooltip : ID individu, âge, cluster
  - Interactif : zoom, pan
- **Cluster descriptions** :
  - Cluster 1 : "Healthy Agers" (35%) - caractéristiques
  - Cluster 2 : "Cardio-Metabolic Risk" (28%)
  - Cluster 3 : "Immune-Hematologic Aging" (22%)
  - Cluster 4 : "Uniform Accelerated Aging" (15%)
- **Stats par cluster** : Âge moyen, gaps moyens par organe

#### 6. **Feature Importance & Explainability**
- **Par organe** : Sélecteur dropdown pour choisir l'organe
- **Bar chart horizontal** : Top 10 features les plus importantes
  - Valeurs d'importance (SHAP ou permutation)
  - Descriptions des biomarqueurs
- **SHAP Summary Plot** (si disponible) : Scatter plot des contributions
- **Insights biologiques** : Explication de pourquoi ces biomarqueurs sont pertinents

#### 7. **Individual Explorer**
- **Search/Select** : Recherche par ID individu ou sélection aléatoire
- **Profile Card** :
  - Âge chronologique
  - Tableau des 5 organes :
    - Biological Age
    - Age Gap (avec badge de couleur : vert/orange/rouge)
    - Status : ✓ Healthy / ~ Normal / ⚠ Advanced
- **Radar Chart** : Profil visuel des 5 age gaps
- **Recommendations** (optionnel) : Messages basés sur les gaps détectés

#### 8. **Limitations & Future Work**
- Section texte structurée :
  - **Limitations** :
    - Cross-sectional data
    - Biomarker selection limitée
    - Population US-specific
    - Pas de causalité établie
  - **Future Directions** :
    - Validation longitudinale
    - Intégration multi-omics
    - Translation clinique
    - Compréhension mécanistique
- Présentation sous forme de cartes avec icônes

#### 9. **About / Documentation**
- Informations sur le projet
- Références scientifiques clés (Belsky, Horvath, Levine)
- Lien vers le repository GitHub
- Instructions pour reproduire l'analyse

---

## Design System & UX

### Design Moderne & Professionnel

**Palette de Couleurs :**
- Primaire : Bleu scientifique (#3B82F6 ou équivalent)
- Secondaire : Violet/Purple pour accents (#8B5CF6)
- Organ-specific colors :
  - Liver : Orange/Amber (#F59E0B)
  - Kidney : Teal (#14B8A6)
  - Cardio-Metabolic : Red/Pink (#EF4444)
  - Immune : Purple (#A855F7)
  - Hematologic : Indigo (#6366F1)
- Statuts :
  - Accelerated : Red (#EF4444)
  - Normal : Gray (#6B7280)
  - Healthy : Green (#10B981)

**Typography :**
- Titres : Inter, Poppins ou Helvetica Neue (bold)
- Body : Inter ou System fonts
- Code/Monospace : Fira Code ou Monaco

**Layout :**
- Navigation top bar fixe avec logo et menu
- Sidebar optionnelle pour navigation rapide
- Sections full-width avec max-width container (1280px)
- Cards avec ombres légères pour les sections de contenu
- Responsive design : Mobile-first

**Interactions :**
- Animations fluides (transitions CSS, Framer Motion)
- Hover effects sur les graphiques
- Tooltips informatifs partout
- Loading states pour les graphiques lourds
- Smooth scroll entre sections

**Accessibilité :**
- WCAG 2.1 AA compliance
- Contraste de couleurs suffisant
- Labels ARIA pour screen readers
- Keyboard navigation

---

## Fonctionnalités Interactives Clés

### Must-Have Features

1. **Filtres globaux** :
   - Filtre par âge (slider 18-80)
   - Filtre par sexe (si disponible dans les données)
   - Filtre par nombre d'organes accélérés
   - Apply/Reset buttons

2. **Exportation de données** :
   - Bouton "Export as CSV" pour les tableaux
   - Bouton "Download Chart as PNG" pour les graphiques
   - Génération de rapport PDF individuel (optionnel, bonus)

3. **Tooltips & Legends** :
   - Tous les graphiques doivent avoir des légendes claires
   - Tooltips au hover avec informations détaillées
   - Info icons (ⓘ) avec explications des termes techniques

4. **Search & Navigation** :
   - Barre de recherche globale pour trouver des individus
   - Table of contents flottante
   - Breadcrumbs pour navigation

5. **Responsive Behavior** :
   - Graphiques qui s'adaptent à la taille d'écran
   - Navigation mobile hamburger menu
   - Touch-friendly sur tablettes

---

## Données à Exporter depuis Python

### Script Python de Génération (à créer)

Crée un nouveau notebook ou script Python `07_export_for_webapp.ipynb` qui :

1. **Charge les données finales** :
   - `age_gaps.parquet`
   - `metrics_summary.json`

2. **Génère les exports JSON** :

```python
# Exemple de structure pour age_gaps.json
{
  "metadata": {
    "n_individuals": 531,
    "organs": ["liver", "kidney", "cardio_metabolic", "immune", "hematologic"],
    "date_generated": "2025-11-23"
  },
  "data": [
    {
      "seqn": "...",
      "age": 54,
      "sex": "M",
      "liver_age_bio": 50.5,
      "liver_age_gap": -3.5,
      "liver_advanced": false,
      "kidney_age_bio": 67.4,
      "kidney_age_gap": 13.4,
      "kidney_advanced": true,
      // ... autres organes
      "max_age_gap": 15.9,
      "n_advanced_organs": 3,
      "cluster": 2
    },
    // ... autres individus
  ],
  "summary_stats": {
    "liver": {"mean": 0.5, "std": 10.2, "min": -25, "max": 30},
    // ... autres organes
  }
}
```

3. **Corrélations** :
```python
# correlations.json
{
  "matrix": [
    [1.0, 0.35, 0.42, 0.15, 0.28],  # liver
    [0.35, 1.0, 0.58, 0.22, 0.31],  # kidney
    // ...
  ],
  "labels": ["liver", "kidney", "cardio_metabolic", "immune", "hematologic"]
}
```

4. **Trajectories** :
```python
# trajectories.json
{
  "age_bins": ["18-30", "30-40", "40-50", "50-60", "60-70", "70-80"],
  "organs": {
    "liver": {
      "mean_gaps": [2.1, 1.8, 0.5, -0.8, -2.3, -4.1],
      "std_gaps": [8.5, 9.2, 10.1, 11.5, 12.8, 14.2],
      "n_individuals": [85, 92, 78, 105, 95, 76]
    },
    // ... autres organes
  }
}
```

5. **Feature Importance** :
```python
# feature_importance/liver.json
{
  "organ": "liver",
  "model": "HistGradientBoosting",
  "features": [
    {
      "name": "LBXSASSI",
      "display_name": "AST (Aspartate Aminotransferase)",
      "importance": 0.25,
      "description": "Marker of liver cell damage",
      "direction": "Higher values → older predicted age"
    },
    {
      "name": "LBXSAL",
      "display_name": "Albumin",
      "importance": 0.18,
      "description": "Reflects liver synthetic function",
      "direction": "Lower values → older predicted age"
    },
    // ... top 10-15 features
  ]
}
```

6. **Clusters** :
```python
# clusters.json
{
  "method": "KMeans (n=4) on UMAP embedding",
  "n_clusters": 4,
  "clusters": [
    {
      "id": 1,
      "name": "Healthy Agers",
      "size": 186,  # 35%
      "percentage": 35.0,
      "description": "All organs aging slower than expected",
      "characteristics": {
        "mean_age": 48.5,
        "mean_gaps": {
          "liver": -5.2,
          "kidney": -4.8,
          "cardio_metabolic": -6.1,
          "immune": -3.9,
          "hematologic": -4.5
        }
      },
      "embedding_center": [2.5, 3.1]  # Centre UMAP/PCA
    },
    // ... autres clusters
  ],
  "embedding": [
    {"seqn": "...", "x": 2.3, "y": 3.5, "cluster": 1},
    // ... tous les points
  ]
}
```

### Fichiers à Fournir à Gemini

Tu devras inclure dans ton prompt pour Gemini :
- Les structures JSON ci-dessus (exemples complets)
- Les valeurs réelles depuis `metrics_summary.json`
- Des exemples de données depuis `age_gaps.parquet` (10-20 lignes)

---

## Instructions de Développement

### Étapes de Réalisation

1. **Setup du projet** :
   - Créer un nouveau projet Next.js avec TypeScript
   - Installer les dépendances (Tailwind, Recharts/Chart.js, D3, etc.)
   - Configurer le layout de base et la navigation

2. **Intégration des données statiques** :
   - Créer le dossier `public/data/`
   - Ajouter tous les fichiers JSON exportés
   - Créer des hooks/services pour charger les données

3. **Développement des pages** :
   - Implémenter chaque section dans l'ordre de priorité :
     1. Home/Executive Summary
     2. Age Gap Analysis (section la plus importante)
     3. Model Performance
     4. Individual Explorer
     5. Clustering/Phenotypes
     6. Feature Importance
     7. Methodology, Limitations, About

4. **Visualisations** :
   - Créer des composants réutilisables pour chaque type de graphique
   - Assurer l'interactivité et les animations
   - Optimiser les performances pour les gros datasets

5. **Polish & Testing** :
   - Tester sur différents navigateurs et tailles d'écran
   - Optimiser le bundle size
   - Ajouter les meta tags SEO
   - Générer la version statique (SSG)

### Structure de Fichiers Recommandée

```
vitalist-web/
├── public/
│   ├── data/                    # Données statiques exportées
│   │   ├── age_gaps.json
│   │   ├── metrics_summary.json
│   │   ├── correlations.json
│   │   ├── trajectories.json
│   │   ├── clusters.json
│   │   ├── individuals/
│   │   └── feature_importance/
│   └── images/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Layout.tsx
│   │   ├── charts/
│   │   │   ├── BarChart.tsx
│   │   │   ├── Heatmap.tsx
│   │   │   ├── LineChart.tsx
│   │   │   ├── RadarChart.tsx
│   │   │   └── ScatterPlot.tsx
│   │   ├── sections/
│   │   │   ├── HeroSection.tsx
│   │   │   ├── ModelPerformance.tsx
│   │   │   ├── AgeGapAnalysis.tsx
│   │   │   ├── ClusteringSection.tsx
│   │   │   └── IndividualExplorer.tsx
│   │   └── ui/
│   │       ├── Card.tsx
│   │       ├── Button.tsx
│   │       ├── Tooltip.tsx
│   │       └── Badge.tsx
│   ├── hooks/
│   │   ├── useAgeGaps.ts
│   │   ├── useMetrics.ts
│   │   └── useFilters.ts
│   ├── types/
│   │   └── data.types.ts
│   ├── utils/
│   │   ├── dataLoader.ts
│   │   └── formatters.ts
│   ├── styles/
│   │   └── globals.css
│   ├── pages/
│   │   ├── index.tsx            # Home
│   │   ├── methodology.tsx
│   │   ├── performance.tsx
│   │   ├── analysis.tsx         # Age gap analysis
│   │   ├── phenotypes.tsx       # Clustering
│   │   ├── explorer.tsx         # Individual explorer
│   │   └── about.tsx
│   └── app/ (si Next.js App Router)
├── tailwind.config.js
├── tsconfig.json
├── next.config.js
└── package.json
```

---

## Livrables Attendus

À la fin, l'application doit :

1. ✅ **Être autonome** : Fonctionne sans backend, uniquement avec données statiques
2. ✅ **Être déployable** : Build optimisé pour hébergement statique
3. ✅ **Être complète** : Toutes les sections décrites ci-dessus implémentées
4. ✅ **Être interactive** : Graphiques, filtres, navigation fluides
5. ✅ **Être professionnelle** : Design moderne, cohérent, accessible
6. ✅ **Être documentée** : README avec instructions d'installation et déploiement

### Bonus (si temps disponible)

- Dark mode toggle
- Génération de rapports PDF individuels
- Animations avancées (Framer Motion)
- Comparaison de 2 individus côte à côte
- Section "FAQ" avec questions courantes
- Tests unitaires (Jest, Testing Library)

---

## Checklist de Qualité

Avant de considérer l'application terminée, vérifier :

- [ ] Toutes les données JSON sont correctement chargées
- [ ] Tous les graphiques sont interactifs et responsifs
- [ ] Les filtres fonctionnent et impactent tous les graphiques
- [ ] La navigation est fluide entre les sections
- [ ] Aucune erreur console
- [ ] Temps de chargement < 3 secondes (Lighthouse score)
- [ ] Responsive design testé sur mobile, tablette, desktop
- [ ] Tous les textes sont clairs et sans fautes
- [ ] Les couleurs respectent les contrastes WCAG
- [ ] Le build statique (SSG) fonctionne sans erreur

---

## Notes Importantes

### Données Réelles

Utilise les **vraies données** du projet Vitalist :
- 531 individus
- 5 organes : liver, kidney, cardio_metabolic, immune, hematologic
- Métriques réelles depuis `metrics_summary.json`
- Age gaps réels depuis `age_gaps.parquet`

### Ton & Style

L'application est destinée à :
- Un **jury technique** (hackathon/compétition)
- Des **chercheurs en biologie du vieillissement**
- Des **data scientists** intéressés par les aging clocks

Le ton doit être :
- **Scientifique mais accessible**
- **Professionnel et crédible**
- **Pédagogique** : expliquer les concepts clés
- **Visuel** : privilégier les graphiques aux longs textes

### Performance

L'application doit être **rapide** :
- Lazy loading des composants lourds
- Memoization des calculs coûteux
- Optimisation des images
- Code splitting automatique (Next.js)
- Compression des JSON (gzip)

---

## Exemples de Textes Clés

### Hero Tagline
**"Discover how your organs age independently. Personalized aging analysis powered by machine learning."**

### Key Finding Cards
1. **"Organs age at different rates"**
   "Within a single individual, some organs can be 10+ years biologically older or younger than chronological age."

2. **"Non-linear models capture complexity"**
   "Gradient boosting models outperform linear baselines by 18-27% in predicting biological age."

3. **"25% show multi-organ acceleration"**
   "One quarter of individuals have 2+ organs with accelerated aging, indicating systemic health risks."

4. **"Distinct aging phenotypes exist"**
   "Population clustering reveals 4 subtypes: Healthy Agers, Cardio-Metabolic Risk, Immune-Hematologic, and Uniform Accelerated."

---

## Question ? Clarifications

Si tu as besoin de clarifications ou de données supplémentaires pour implémenter certaines fonctionnalités, demande-moi et je te fournirai les exports JSON nécessaires ou des précisions sur les visualisations attendues.

**Objectif final** : Une web app moderne, interactive, et visuellement impressionnante qui remplace complètement le notebook 06 et permet à un jury de comprendre le projet Vitalist en 10-15 minutes de navigation.

Bonne chance ! 🚀
