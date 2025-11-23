# Guide de Création de la Web App Vitalist

Ce guide explique comment créer l'application web complète qui remplace le notebook 06.

## Vue d'ensemble

L'application web sera une **Single Page Application (SPA)** moderne avec approche **Static Data Export**, permettant de visualiser et explorer tous les résultats du projet Vitalist de manière interactive.

## Étapes de Réalisation

### 1️⃣ Exporter les Données (Python → JSON)

**Exécuter le notebook d'export :**

```bash
jupyter notebook notebooks/07_export_for_webapp.ipynb
```

Ce notebook va :
- Charger toutes les données processed
- Générer des fichiers JSON optimisés pour le web
- Créer la structure `web_app/public/data/`

**Outputs générés :**
```
web_app/public/data/
├── age_gaps.json              # Données complètes (531 individus × 5 organes)
├── metrics_summary.json       # Performances des modèles ML
├── correlations.json          # Matrice de corrélation inter-organes
├── trajectories.json          # Trajectoires pseudo-longitudinales
├── clusters.json              # Résultats du clustering UMAP/PCA
├── feature_importance/        # Importance des biomarqueurs
│   ├── liver.json
│   ├── kidney.json
│   ├── cardio_metabolic.json
│   ├── immune.json
│   └── hematologic.json
└── individuals/               # Profils individuels (échantillon)
    ├── 0.json
    ├── 1.json
    └── ...
```

### 2️⃣ Préparer le Prompt pour Gemini 3

**Fichier à utiliser :** `PROMPT_GEMINI_WEB_APP.md`

Ce prompt contient :
- ✅ Contexte complet du projet Vitalist
- ✅ Spécifications techniques (React/Next.js + TypeScript + Tailwind)
- ✅ Structure détaillée de l'application (9 sections)
- ✅ Design system et palette de couleurs
- ✅ Fonctionnalités interactives requises
- ✅ Exemples de structures de données JSON
- ✅ Instructions de développement

**Comment l'utiliser :**

1. Ouvrir `PROMPT_GEMINI_WEB_APP.md`
2. **Personnaliser si nécessaire** :
   - Remplacer les valeurs d'exemple par les vraies données (depuis age_gaps.json)
   - Ajuster les couleurs ou le design system
   - Ajouter/retirer des fonctionnalités
3. Copier l'intégralité du prompt
4. Coller dans Gemini 3 (ou Claude Projects, ou Cursor AI)

### 3️⃣ Générer l'Application Web

**Option A : Avec Gemini 3 (recommandé)**

```
1. Ouvrir Gemini 3
2. Coller le contenu de PROMPT_GEMINI_WEB_APP.md
3. Ajouter : "Génère le projet Next.js complet avec tous les fichiers"
4. Gemini va créer :
   - Structure de fichiers
   - Composants React
   - Pages
   - Hooks et utils
   - Configuration (tailwind.config.js, etc.)
```

**Option B : Développement manuel**

Si Gemini génère seulement la structure, développer manuellement en suivant :
- Le prompt comme spécification complète
- Les exemples de code fournis
- L'ordre de priorité des sections

### 4️⃣ Intégrer les Données

Une fois le projet Next.js créé :

```bash
# Copier les données exportées
cp -r web_app/public/data/ <nextjs_project>/public/data/

# Ou si la structure n'existe pas encore
mkdir -p <nextjs_project>/public
cp -r web_app/public/data/ <nextjs_project>/public/
```

### 5️⃣ Installer et Lancer l'Application

```bash
cd <nextjs_project>

# Installer les dépendances
npm install
# ou
yarn install

# Lancer en développement
npm run dev
# ou
yarn dev

# Ouvrir http://localhost:3000
```

### 6️⃣ Build et Déploiement

**Build statique :**

```bash
npm run build
npm run export  # Pour Next.js avec static export
```

**Déployer sur Vercel (recommandé pour Next.js) :**

```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
vercel
```

**Alternatives de déploiement :**
- **Netlify** : Drag & drop du dossier `out/`
- **GitHub Pages** : Push du dossier `out/` sur branche gh-pages
- **Cloudflare Pages** : Connect GitHub repo

---

## Structure de l'Application Web

### Pages Principales

1. **Home / Executive Summary** - Vue d'ensemble avec KPIs
2. **Methodology & Data** - Explication du projet et pipeline
3. **Model Performance** - Comparaison Linear vs Gradient Boosting
4. **Age Gap Analysis** ⭐ (Section principale)
   - Distributions des gaps
   - Corrélations inter-organes
   - Patterns de vieillissement accéléré
   - Trajectoires pseudo-longitudinales
5. **Aging Phenotypes** - Clustering et profils
6. **Feature Importance** - Explicabilité des modèles
7. **Individual Explorer** - Profils individuels interactifs
8. **Limitations & Future Work** - Contexte scientifique
9. **About** - Documentation et références

### Fonctionnalités Clés

- ✅ **Filtres interactifs** : Âge, sexe, nombre d'organes accélérés
- ✅ **Visualisations** : Charts interactifs (Recharts/D3.js)
- ✅ **Export de données** : CSV, PNG des graphiques
- ✅ **Responsive design** : Mobile, tablette, desktop
- ✅ **Performance** : Lazy loading, code splitting
- ✅ **Accessibilité** : WCAG 2.1 AA

---

## Personnalisation Rapide

### Couleurs par Organe

Modifier dans `tailwind.config.js` ou dans le design system :

```javascript
const organColors = {
  liver: '#F59E0B',        // Orange/Amber
  kidney: '#14B8A6',       // Teal
  cardio_metabolic: '#EF4444',  // Red
  immune: '#A855F7',       // Purple
  hematologic: '#6366F1'   // Indigo
}
```

### Ajouter une Nouvelle Section

1. Créer un composant dans `src/components/sections/`
2. Ajouter la route dans `src/pages/` (ou App Router)
3. Ajouter au menu de navigation

### Modifier les Seuils

Par défaut : Age Gap > +5 ans = vieillissement accéléré

Modifier dans `src/utils/thresholds.ts` :

```typescript
export const THRESHOLDS = {
  advanced: 5.0,   // Gap > +5 ans
  healthy: -5.0    // Gap < -5 ans
}
```

---

## Checklist de Validation

Avant de considérer l'application terminée :

- [ ] **Données chargées** : Tous les JSON se chargent sans erreur
- [ ] **Visualisations** : Tous les graphiques s'affichent correctement
- [ ] **Interactivité** : Tooltips, filtres, hover effects fonctionnent
- [ ] **Responsive** : Testé sur mobile, tablette, desktop
- [ ] **Performance** : Lighthouse score > 90
- [ ] **Navigation** : Tous les liens et sections accessibles
- [ ] **Accessibilité** : Contrastes OK, navigation clavier OK
- [ ] **Build** : `npm run build` sans erreur
- [ ] **Deploy** : Application accessible en ligne

---

## Dépendances Principales

Le prompt spécifie ces technologies :

**Core :**
- Next.js 14+ avec App Router (ou Pages Router)
- React 18+
- TypeScript

**UI/Styling :**
- Tailwind CSS
- shadcn/ui ou Material-UI

**Charting :**
- Recharts (graphiques simples)
- D3.js (visualisations complexes)
- Plotly.js (optionnel, pour interactivité avancée)

**Utils :**
- date-fns ou dayjs (manipulation dates)
- lodash-es (utilitaires)

---

## Troubleshooting

### Les données JSON ne se chargent pas

**Solution :**
- Vérifier que les fichiers sont dans `public/data/`
- Next.js : accès via `/data/age_gaps.json` (pas `/public/...`)
- Vérifier la console navigateur pour erreurs 404

### Erreur de build

**Solution :**
```bash
# Nettoyer et rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Graphiques ne s'affichent pas

**Solution :**
- Vérifier que les données ont la bonne structure
- Console pour erreurs JS
- Tester avec données mock d'abord

### Performance lente

**Solutions :**
- Activer lazy loading pour les graphiques lourds
- Utiliser `React.memo()` sur les composants
- Implementer virtualisation pour listes longues (react-window)
- Compresser les JSON (gzip dans Vercel/Netlify fait ça automatiquement)

---

## Ressources Utiles

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Recharts](https://recharts.org/)
- [D3.js](https://d3js.org/)

### Exemples de Dashboards
- [shadcn/ui Dashboard](https://ui.shadcn.com/examples/dashboard)
- [Vercel Analytics](https://vercel.com/analytics)

### Design Inspiration
- [Dribbble - Data Dashboards](https://dribbble.com/search/data-dashboard)
- [Behance - Scientific Dashboards](https://www.behance.net/search/projects/scientific%20dashboard)

---

## Support

Pour questions ou problèmes :
1. Revoir le prompt complet dans `PROMPT_GEMINI_WEB_APP.md`
2. Vérifier la structure des données dans `web_app/public/data/`
3. Consulter les exemples de code dans le prompt
4. Ajuster les spécifications selon vos besoins

---

## Exemple de Prompt Itératif pour Gemini

Si Gemini ne génère pas tout en une fois, itérer :

```
Session 1: "Génère la structure de base du projet Next.js avec navigation"
Session 2: "Génère le composant AgeGapAnalysis avec tous les graphiques"
Session 3: "Génère le composant IndividualExplorer avec profils"
Session 4: "Ajoute les filtres globaux et l'export CSV"
...
```

---

**Bonne création ! 🚀**

L'objectif est d'avoir une web app moderne, interactive et professionnelle qui impressionne le jury et remplace complètement le notebook 06 Jupyter.
