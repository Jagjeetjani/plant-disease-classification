import os
import json
import numpy as np
from PIL import Image
import cv2

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(PROJECT_DIR, "models")
SAMPLES_DIR = os.path.join(PROJECT_DIR, "sample_leaves")
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(DATASET_DIR, exist_ok=True)

DISEASE_DB = {
    "Tomato___Early_blight": {
        "crop": "Tomato",
        "condition": "Early Blight",
        "scientific_name": "Solanum lycopersicum",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": "Dark brown to black necrotic spots with characteristic concentric target-board rings on older foliage, surrounded by chlorotic yellow halos.",
        "favorable_conditions": "Warm temperatures (24-29°C) combined with high humidity, heavy dew, or overhead irrigation.",
        "severity": "High (Yield loss up to 50-70% if unmanaged)",
        "chemical_treatment": "Apply Chlorothalonil (0.2%), Mancozeb (0.25%), or Azoxystrobin at 7-10 day intervals upon first appearance.",
        "organic_remedy": "Foliar application of Copper octanoate (copper soap) or Bacillus subtilis (Serenade). Weekly neem oil (0.5%) emulsion.",
        "cultural_prevention": "Stake plants for air circulation, avoid overhead sprinkler watering, practice 3-year crop rotation with non-solanaceous crops, and mulch base.",
        "visual_profile": {"shape": "compound_serrated", "base_color": [34, 139, 34], "lesion_color": [50, 30, 20], "lesion_style": "target_rings", "chlorosis": True}
    },
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "condition": "Late Blight",
        "scientific_name": "Solanum lycopersicum",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": "Rapidly expanding water-soaked dark olive to black lesions with pale green borders; white fuzzy sporulation under leaf surface in humid conditions.",
        "favorable_conditions": "Cool, moist weather (15-22°C) with persistent leaf wetness and relative humidity >90%.",
        "severity": "Critical (Total crop destruction possible within 7-14 days)",
        "chemical_treatment": "Systemic fungicides: Metalaxyl + Mancozeb (Ridomil Gold 2g/L), Cymoxanil, or Dimethomorph.",
        "organic_remedy": "Fixed copper fungicides (Bordeaux mixture 1%) applied protectively before rain events.",
        "cultural_prevention": "Destroy infected volunteer plants, ensure wide row spacing, use certified disease-free transplants, and install drip irrigation.",
        "visual_profile": {"shape": "compound_serrated", "base_color": [46, 125, 50], "lesion_color": [25, 30, 25], "lesion_style": "water_soaked", "chlorosis": False}
    },
    "Tomato___Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "condition": "Yellow Leaf Curl Virus",
        "scientific_name": "Solanum lycopersicum",
        "pathogen": "Tomato Yellow Leaf Curl Begomovirus (TYLCV)",
        "symptoms": "Severe upward leaf cupping, curling, interveinal chlorosis (yellowing), marked leaf reduction, and stunted bush growth with flower drop.",
        "favorable_conditions": "Warm climates favoring high populations of the whitefly vector (Bemisia tabaci).",
        "severity": "High (Causes near 100% loss if infection occurs before flowering)",
        "chemical_treatment": "No direct cure for viral infection. Vector control: Imidacloprid (0.3ml/L), Thiamethoxam, or Acetamiprid to suppress whiteflies.",
        "organic_remedy": "Yellow sticky traps (20-25 traps/acre), insecticidal potassium soap spray, and neem kernel extract (5%).",
        "cultural_prevention": "Install 50-mesh insect-proof netting in greenhouses, remove infected plants immediately, and plant TYLCV-resistant varieties.",
        "visual_profile": {"shape": "compound_curled", "base_color": [154, 205, 50], "lesion_color": [220, 220, 80], "lesion_style": "curled_yellow", "chlorosis": True}
    },
    "Tomato___healthy": {
        "crop": "Tomato",
        "condition": "Healthy Leaf",
        "scientific_name": "Solanum lycopersicum",
        "pathogen": "None (Pristine Plant State)",
        "symptoms": "Uniform deep green coloration, well-defined venation, firm turgid foliage, and no necrotic lesions or chlorosis.",
        "favorable_conditions": "Optimum sunlight (6-8 hours daily), balanced N-P-K (10-10-10) fertilization, and soil pH 6.2-6.8.",
        "severity": "None (Healthy productive crop)",
        "chemical_treatment": "No chemical intervention needed. Maintain routine agronomic monitoring.",
        "organic_remedy": "Prophylactic compost tea and seaweed extract foliar spray for boosted plant immunity.",
        "cultural_prevention": "Standard crop management, consistent watering, and regular scouting.",
        "visual_profile": {"shape": "compound_serrated", "base_color": [34, 139, 34], "lesion_color": None, "lesion_style": "none", "chlorosis": False}
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "condition": "Early Blight",
        "scientific_name": "Solanum tuberosum",
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": "Brown, angular target-board lesions delimited by major veins, with yellow chlorotic halos on lower mature leaflets.",
        "favorable_conditions": "Alternating wet and dry periods, warm temperatures (22-30°C), and stressed crop canopy.",
        "severity": "Moderate to High (Premature defoliation and tuber size reduction)",
        "chemical_treatment": "Mancozeb 75 WP (2g/L), Propineb, or Difenoconazole (0.5ml/L) at tuber initiation.",
        "organic_remedy": "Copper hydroxide spray and Trichoderma viride biological antagonist soil application.",
        "cultural_prevention": "Ensure adequate nitrogen and potassium fertility; avoid sprinkler irrigation late in the afternoon.",
        "visual_profile": {"shape": "oval_pinnate", "base_color": [46, 139, 87], "lesion_color": [45, 28, 15], "lesion_style": "target_rings", "chlorosis": True}
    },
    "Potato___Late_blight": {
        "crop": "Potato",
        "condition": "Late Blight",
        "scientific_name": "Solanum tuberosum",
        "pathogen": "Phytophthora infestans (Oomycete)",
        "symptoms": "Large, irregular water-soaked pale-to-dark brown spots near leaf margins, rapidly coalescing into black dead tissue with white mildew.",
        "favorable_conditions": "Temperatures 10-20°C with relative humidity above 90% for prolonged intervals.",
        "severity": "Devastating (Historical cause of the Great Irish Famine; rapid total loss)",
        "chemical_treatment": "Preventative: Mancozeb (2.5g/L). Curative: Cymoxanil + Mancozeb (Curzate 2g/L) or Fenamidone.",
        "organic_remedy": "Bordeaux mixture (1%) protective coverage; harvest haulm destruction before lifting tubers.",
        "cultural_prevention": "Plant certified seed tubers, hill potatoes well to protect tubers, and eliminate cull piles.",
        "visual_profile": {"shape": "oval_pinnate", "base_color": [40, 110, 60], "lesion_color": [20, 25, 20], "lesion_style": "water_soaked", "chlorosis": False}
    },
    "Potato___healthy": {
        "crop": "Potato",
        "condition": "Healthy Leaf",
        "scientific_name": "Solanum tuberosum",
        "pathogen": "None (Pristine Plant State)",
        "symptoms": "Lush vibrant emerald leaflets, smooth margin texture, robust vein structural integrity, no spot deformities.",
        "favorable_conditions": "Cool season conditions (15-20°C), deep loose well-drained loamy soil, balanced irrigation.",
        "severity": "None (Optimal vegetative vigour)",
        "chemical_treatment": "None required.",
        "organic_remedy": "Soil beneficial mycorrhizal fungi application.",
        "cultural_prevention": "Proper hilling, weed suppression, balanced nitrogen management.",
        "visual_profile": {"shape": "oval_pinnate", "base_color": [34, 139, 34], "lesion_color": None, "lesion_style": "none", "chlorosis": False}
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)",
        "condition": "Common Rust",
        "scientific_name": "Zea mays",
        "pathogen": "Puccinia sorghi (Fungus)",
        "symptoms": "Elongated golden-brown to cinnamon-brown pustules (uredinia) scattered abundantly on both upper and lower leaf surfaces; ruptures epidermis with powdery spores.",
        "favorable_conditions": "Cool to moderate temperatures (16-25°C) and high relative humidity (>95%).",
        "severity": "Moderate (Yield reduction of 10-25% in susceptible grain hybrids)",
        "chemical_treatment": "Azoxystrobin + Difenoconazole (Amistar Top 1ml/L) or Pyraclostrobin at first tassel emergence.",
        "organic_remedy": "Sulfur dusting (80% WP) or biological treatment with Ampelomyces quisqualis hyperparasite.",
        "cultural_prevention": "Select rust-resistant hybrids (Rp single-gene resistance), early planting to escape late spore showers.",
        "visual_profile": {"shape": "elongated_blade", "base_color": [60, 140, 40], "lesion_color": [160, 80, 20], "lesion_style": "rust_pustules", "chlorosis": True}
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)",
        "condition": "Northern Leaf Blight",
        "scientific_name": "Zea mays",
        "pathogen": "Exserohilum turcicum (Fungus)",
        "symptoms": "Long, elliptical cigar-shaped grayish-green to tan lesions (2.5-15 cm long) with distinctive tapered ends, parallel to leaf veins.",
        "favorable_conditions": "Moderate temperatures (18-27°C) accompanied by extended periods of heavy dew.",
        "severity": "High (Severe defoliation leading to grain fill failure and stalk rot)",
        "chemical_treatment": "Propiconazole 25 EC (1ml/L), Mancozeb, or Pyraclostrobin applied at VT-R1 growth stages.",
        "organic_remedy": "Bio-fungicide sprays containing Bacillus amyloliquefaciens and silicon-based foliar enhancers.",
        "cultural_prevention": "Tillage to bury residue, 2-year crop rotation with soybeans, and deployment of Ht-gene resistant hybrids.",
        "visual_profile": {"shape": "elongated_blade", "base_color": [50, 130, 45], "lesion_color": [130, 110, 70], "lesion_style": "cigar_lesions", "chlorosis": False}
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)",
        "condition": "Healthy Leaf",
        "scientific_name": "Zea mays",
        "pathogen": "None (Pristine Plant State)",
        "symptoms": "Broad, elongated ribbon-like blade with prominent central whitish-green midrib; rich uniform chlorophyll density.",
        "favorable_conditions": "Full sun, warm temperatures (21-32°C), consistent soil moisture during vegetative growth.",
        "severity": "None (Optimal photosynthetic canopy)",
        "chemical_treatment": "None required.",
        "organic_remedy": "Foliar zinc and boron micronutrient supplementation.",
        "cultural_prevention": "Optimal planting density (65,000-75,000 plants/ha) and weed canopy control.",
        "visual_profile": {"shape": "elongated_blade", "base_color": [40, 135, 40], "lesion_color": None, "lesion_style": "none", "chlorosis": False}
    },
    "Apple___Apple_scab": {
        "crop": "Apple",
        "condition": "Apple Scab",
        "scientific_name": "Malus domestica",
        "pathogen": "Venturia inaequalis (Fungus)",
        "symptoms": "Olive-green to dull velvety black circular lesions with feathery margins; leaf tissue distorts, curls, and drops prematurely.",
        "favorable_conditions": "Spring wetness periods (Mills infection table) with temperatures between 13-24°C.",
        "severity": "High (Fruit deformities and up to 70% unmarketable crop)",
        "chemical_treatment": "Captan 50 WP (2.5g/L), Difenoconazole, Myclobutanil, or Dodine timed around rain events.",
        "organic_remedy": "Lime sulfur or wettable sulfur applied pre-bloom; potassium bicarbonate spray.",
        "cultural_prevention": "Rake and shred fallen leaves in autumn to eliminate pseudothecia overwintering.",
        "visual_profile": {"shape": "ovate_serrate", "base_color": [50, 130, 60], "lesion_color": [40, 45, 30], "lesion_style": "velvety_spots", "chlorosis": True}
    },
    "Apple___Black_rot": {
        "crop": "Apple",
        "condition": "Black Rot (Frog-Eye Leaf Spot)",
        "scientific_name": "Malus domestica",
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "symptoms": "Small purple spots developing into 'frog-eye' lesions with tan centres and dark purple-brown concentric borders.",
        "favorable_conditions": "Warm temperatures (26-28°C) following rainy periods during bloom and early petal fall.",
        "severity": "Moderate to Severe (Branch cankers, leaf defoliation, and mummified black fruit)",
        "chemical_treatment": "Thiophanate-methyl, Captan, or Strobilurin fungicides applied from pink bud stage.",
        "organic_remedy": "Liquid copper applied at bud break; bio-protective Bacillus subtilis strains.",
        "cultural_prevention": "Prune out dead wood, mummified fruits, and fire blight cankers which harbor spores.",
        "visual_profile": {"shape": "ovate_serrate", "base_color": [45, 120, 50], "lesion_color": [70, 30, 25], "lesion_style": "frog_eye", "chlorosis": True}
    },
    "Apple___healthy": {
        "crop": "Apple",
        "condition": "Healthy Leaf",
        "scientific_name": "Malus domestica",
        "pathogen": "None (Pristine Plant State)",
        "symptoms": "Glossy ovate foliage, finely serrated margin, vivid chlorophyll saturation without blemishes.",
        "favorable_conditions": "Chilling requirement met in winter, 6-8 hrs full sunlight, well-aerated loam soil.",
        "severity": "None (Healthy orchard canopy)",
        "chemical_treatment": "None required.",
        "organic_remedy": "Foliar kelp extract and calcium nitrate sprays for cell wall strengthening.",
        "cultural_prevention": "Annual dormant pruning for sunlight penetration and canopy aeration.",
        "visual_profile": {"shape": "ovate_serrate", "base_color": [34, 139, 34], "lesion_color": None, "lesion_style": "none", "chlorosis": False}
    },
    "Pepper__bell___Bacterial_spot": {
        "crop": "Bell Pepper",
        "condition": "Bacterial Spot",
        "scientific_name": "Capsicum annuum",
        "pathogen": "Xanthomonas campestris pv. vesicatoria (Bacterium)",
        "symptoms": "Small, water-soaked, angular blistering spots on leaf undersides, becoming dark brown with greasy texture and pale yellow halos.",
        "favorable_conditions": "High temperatures (24-30°C) with frequent rainfall, overhead irrigation, and wind-driven rain.",
        "severity": "High (Severe leaf drop exposes fruit to sunscald; significant yield collapse)",
        "chemical_treatment": "Copper hydroxide (Kocide 2g/L) tank-mixed with Mancozeb (to combat copper-resistant bacterial strains).",
        "organic_remedy": "Bacteriophage treatments (AgriPhage), Bacillus amyloliquefaciens, and potassium silicate.",
        "cultural_prevention": "Use hot water treated seeds (50°C for 25 min), avoid working in wet foliage, and rotate away from solanaceous crops for 2 years.",
        "visual_profile": {"shape": "ovate_lanceolate", "base_color": [40, 130, 50], "lesion_color": [50, 40, 20], "lesion_style": "bacterial_angular", "chlorosis": True}
    },
    "Pepper__bell___healthy": {
        "crop": "Bell Pepper",
        "condition": "Healthy Leaf",
        "scientific_name": "Capsicum annuum",
        "pathogen": "None (Pristine Plant State)",
        "symptoms": "Smooth, lanceolate to ovate leaf blade with unbroken glossy cuticle, vibrant green color, strong petiolar connection.",
        "favorable_conditions": "Warm growing season (21-28°C), steady drip moisture, magnesium and calcium supplemented soil.",
        "severity": "None (Optimal vegetative vigour)",
        "chemical_treatment": "None required.",
        "organic_remedy": "Epsom salt (magnesium sulfate) foliar spray for enhanced chlorophyll synthesis.",
        "cultural_prevention": "Plastic mulch, drip fertigation, and regular scouting.",
        "visual_profile": {"shape": "ovate_lanceolate", "base_color": [35, 135, 45], "lesion_color": None, "lesion_style": "none", "chlorosis": False}
    }
}

# Save database JSON
with open(os.path.join(MODELS_DIR, "disease_database.json"), "w") as f:
    json.dump(DISEASE_DB, f, indent=4)
print("Saved disease database with", len(DISEASE_DB), "classes.")

def generate_realistic_leaf_image(class_key, size=(224, 224), seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    meta = DISEASE_DB[class_key]
    profile = meta["visual_profile"]
    w, h = size
    
    # 1. Background: PlantVillage style neutral laboratory paper / bench
    bg_brightness = np.random.randint(185, 215)
    bg_noise = np.random.normal(0, 3, (h, w, 3)).astype(np.float32)
    img_np = np.full((h, w, 3), bg_brightness, dtype=np.float32) + bg_noise
    img_np = np.clip(img_np, 0, 255).astype(np.uint8)
    
    # 2. Leaf Mask & Silhouette
    mask = np.zeros((h, w), dtype=np.uint8)
    shape_type = profile["shape"]
    cx, cy = w // 2, h // 2
    
    if shape_type in ["compound_serrated", "compound_curled"]:
        pts = []
        for deg in range(0, 360, 4):
            rad = np.radians(deg)
            rx = w * 0.32 * (1.0 + 0.15 * np.cos(rad) - 0.1 * np.sin(2 * rad))
            ry = h * 0.40 * (1.0 - 0.25 * np.cos(rad))
            lobe = 1.0 + 0.12 * np.cos(6 * rad) + 0.05 * np.sin(14 * rad)
            x = int(cx + rx * np.cos(rad) * lobe)
            y = int(cy + ry * np.sin(rad) * lobe)
            pts.append([x, y])
        cv2.fillPoly(mask, [np.array(pts)], 255)
        cv2.line(mask, (cx, int(cy + h * 0.38)), (cx - 15, int(h * 0.95)), 255, thickness=int(w * 0.025))

    elif shape_type == "oval_pinnate":
        pts = []
        for deg in range(0, 360, 4):
            rad = np.radians(deg)
            rx = w * 0.35 * (1.0 - 0.1 * np.cos(rad))
            ry = h * 0.42 * (1.0 - 0.2 * np.cos(rad))
            wavy = 1.0 + 0.04 * np.sin(8 * rad)
            x = int(cx + rx * np.cos(rad) * wavy)
            y = int(cy + ry * np.sin(rad) * wavy)
            pts.append([x, y])
        cv2.fillPoly(mask, [np.array(pts)], 255)
        cv2.line(mask, (cx, int(cy + h * 0.38)), (cx, int(h * 0.96)), 255, thickness=int(w * 0.03))

    elif shape_type == "elongated_blade":
        pts = [
            [cx, int(h * 0.08)],
            [int(cx + w * 0.25), int(h * 0.35)],
            [int(cx + w * 0.28), int(h * 0.65)],
            [int(cx + w * 0.18), int(h * 0.96)],
            [int(cx - w * 0.18), int(h * 0.96)],
            [int(cx - w * 0.28), int(h * 0.65)],
            [int(cx - w * 0.25), int(h * 0.35)],
        ]
        cv2.fillPoly(mask, [np.array(pts)], 255)

    elif shape_type == "ovate_serrate":
        pts = []
        for deg in range(0, 360, 3):
            rad = np.radians(deg)
            rx = w * 0.33 * (1.0 - 0.12 * np.cos(rad))
            ry = h * 0.39 * (1.0 - 0.18 * np.cos(rad))
            serrate = 1.0 + 0.06 * np.cos(20 * rad)
            x = int(cx + rx * np.cos(rad) * serrate)
            y = int(cy + ry * np.sin(rad) * serrate)
            pts.append([x, y])
        cv2.fillPoly(mask, [np.array(pts)], 255)
        cv2.line(mask, (cx, int(cy + h * 0.36)), (cx + 5, int(h * 0.94)), 255, thickness=int(w * 0.025))

    else: # ovate_lanceolate
        pts = []
        for deg in range(0, 360, 4):
            rad = np.radians(deg)
            rx = w * 0.30 * (1.0 - 0.15 * np.cos(rad))
            ry = h * 0.44 * (1.0 - 0.30 * np.cos(rad))
            x = int(cx + rx * np.cos(rad))
            y = int(cy + ry * np.sin(rad))
            pts.append([x, y])
        cv2.fillPoly(mask, [np.array(pts)], 255)
        cv2.line(mask, (cx, int(cy + h * 0.40)), (cx - 8, int(h * 0.95)), 255, thickness=int(w * 0.025))

    mask = cv2.GaussianBlur(mask, (5, 5), 1.0)
    leaf_bool = mask > 120
    
    # 3. Base Leaf Pigmentation
    base_rgb = np.array(profile["base_color"], dtype=np.float32)
    texture = np.random.normal(0, 6, (h, w, 3)).astype(np.float32)
    y_grad, x_grad = np.mgrid[0:h, 0:w]
    light = 1.0 + 0.10 * ((cx - x_grad) + (cy - y_grad)) / float(w)
    light = np.expand_dims(light, axis=-1)
    
    leaf_rgb = (base_rgb * light + texture)
    leaf_rgb = np.clip(leaf_rgb, 20, 240)
    
    # 4. Chlorosis
    if profile.get("chlorosis", False):
        yellow_rgb = np.array([210, 200, 60], dtype=np.float32)
        if profile["lesion_style"] == "curled_yellow":
            yellow_map = np.sin(x_grad / 15.0) * np.cos(y_grad / 15.0) + np.random.normal(0, 0.4, (h, w))
            yellow_mask = (yellow_map > 0.1).astype(np.float32)[:, :, np.newaxis]
            leaf_rgb = leaf_rgb * (1.0 - yellow_mask * 0.75) + yellow_rgb * (yellow_mask * 0.75)
        else:
            yellow_map = np.random.uniform(0.1, 0.4, (h, w, 1)).astype(np.float32)
            leaf_rgb = leaf_rgb * 0.75 + yellow_rgb * 0.25

    # 5. Venation
    vein_color = (base_rgb * 1.25).clip(0, 255).astype(np.uint8)
    vein_canvas = np.zeros((h, w, 3), dtype=np.uint8)
    if shape_type == "elongated_blade":
        for offset in range(-int(w * 0.18), int(w * 0.18), 12):
            cv2.line(vein_canvas, (cx + offset, int(h * 0.15)), (cx + offset + int(offset * 0.1), int(h * 0.95)), vein_color.tolist(), 1)
        cv2.line(vein_canvas, (cx, int(h * 0.08)), (cx, int(h * 0.96)), [int(c) for c in (base_rgb * 1.4).clip(0, 255)], 3)
    else:
        cv2.line(vein_canvas, (cx, int(h * 0.12)), (cx, int(h * 0.92)), vein_color.tolist(), 2)
        for y_v in range(int(h * 0.25), int(h * 0.80), 22):
            cv2.line(vein_canvas, (cx, y_v), (int(cx - w * 0.22), int(y_v - 18)), vein_color.tolist(), 1)
            cv2.line(vein_canvas, (cx, y_v), (int(cx + w * 0.22), int(y_v - 18)), vein_color.tolist(), 1)
            
    vein_mask = (vein_canvas.sum(axis=-1) > 0) & leaf_bool
    leaf_rgb[vein_mask] = vein_canvas[vein_mask]

    # 6. Disease Lesions
    lesion_style = profile.get("lesion_style", "none")
    lesion_color = profile.get("lesion_color")
    
    if lesion_style != "none" and lesion_color is not None:
        lesion_rgb = np.array(lesion_color, dtype=np.float32)
        
        if lesion_style == "target_rings":
            num_lesions = np.random.randint(4, 8)
            for _ in range(num_lesions):
                lx = int(cx + np.random.uniform(-0.20, 0.20) * w)
                ly = int(cy + np.random.uniform(-0.22, 0.22) * h)
                if mask[ly, lx] > 180:
                    max_r = np.random.randint(12, 24)
                    cv2.circle(leaf_rgb, (lx, ly), int(max_r * 1.5), (200, 190, 50), -1)
                    for r in range(max_r, 2, -4):
                        ring_c = (lesion_rgb * (0.85 if (r // 4) % 2 == 0 else 1.15)).clip(0, 255)
                        cv2.circle(leaf_rgb, (lx, ly), r, ring_c.tolist(), -1)
                        
        elif lesion_style == "water_soaked":
            num_patches = np.random.randint(3, 5)
            for _ in range(num_patches):
                lx = int(cx + np.random.uniform(-0.24, 0.24) * w)
                ly = int(cy + np.random.uniform(-0.26, 0.26) * h)
                rx = np.random.randint(18, 36)
                ry = np.random.randint(14, 28)
                angle = np.random.randint(0, 180)
                cv2.ellipse(leaf_rgb, (lx, ly), (rx, ry), angle, 0, 360, (lesion_rgb * 0.9).tolist(), -1)
                cv2.ellipse(leaf_rgb, (lx, ly), (rx + 3, ry + 3), angle, 0, 360, (140, 150, 130), 2)

        elif lesion_style == "rust_pustules":
            num_pustules = np.random.randint(25, 45)
            for _ in range(num_pustules):
                px = int(cx + np.random.uniform(-0.18, 0.18) * w)
                py = int(cy + np.random.uniform(-0.32, 0.32) * h)
                if mask[py, px] > 180:
                    cv2.ellipse(leaf_rgb, (px, py), (4, 7), 0, 0, 360, (190, 90, 25), -1)
                    cv2.ellipse(leaf_rgb, (px, py), (2, 4), 0, 0, 360, (130, 50, 15), -1)

        elif lesion_style == "cigar_lesions":
            num_cigars = np.random.randint(3, 5)
            for _ in range(num_cigars):
                lx = int(cx + np.random.uniform(-0.16, 0.16) * w)
                ly = int(cy + np.random.uniform(-0.28, 0.28) * h)
                length = np.random.randint(30, 55)
                width = np.random.randint(6, 11)
                cv2.ellipse(leaf_rgb, (lx, ly), (width, length), 0, 0, 360, (150, 130, 90), -1)
                cv2.ellipse(leaf_rgb, (lx, ly), (width + 2, length + 2), 0, 0, 360, (110, 90, 60), 1)

        elif lesion_style == "velvety_spots":
            num_spots = np.random.randint(6, 12)
            for _ in range(num_spots):
                sx = int(cx + np.random.uniform(-0.20, 0.20) * w)
                sy = int(cy + np.random.uniform(-0.22, 0.22) * h)
                if mask[sy, sx] > 180:
                    sr = np.random.randint(6, 15)
                    cv2.circle(leaf_rgb, (sx, sy), sr + 2, (180, 180, 70), -1)
                    cv2.circle(leaf_rgb, (sx, sy), sr, (35, 45, 25), -1)

        elif lesion_style == "frog_eye":
            num_eyes = np.random.randint(5, 8)
            for _ in range(num_eyes):
                ex = int(cx + np.random.uniform(-0.20, 0.20) * w)
                ey = int(cy + np.random.uniform(-0.22, 0.22) * h)
                if mask[ey, ex] > 180:
                    er = np.random.randint(8, 15)
                    cv2.circle(leaf_rgb, (ex, ey), er, (80, 35, 30), -1)
                    cv2.circle(leaf_rgb, (ex, ey), int(er * 0.55), (195, 175, 140), -1)
                    cv2.circle(leaf_rgb, (ex, ey), 2, (50, 20, 20), -1)

        elif lesion_style == "bacterial_angular":
            num_spots = np.random.randint(14, 25)
            for _ in range(num_spots):
                bx = int(cx + np.random.uniform(-0.18, 0.18) * w)
                by = int(cy + np.random.uniform(-0.28, 0.28) * h)
                if mask[by, bx] > 180:
                    br = np.random.randint(3, 6)
                    cv2.circle(leaf_rgb, (bx, by), br + 2, (190, 185, 60), -1)
                    cv2.rectangle(leaf_rgb, (bx - br, by - br), (bx + br, by + br), (45, 35, 15), -1)

    # 7. Blend Leaf onto Background
    mask_3d = np.repeat(np.expand_dims(mask / 255.0, axis=-1), 3, axis=-1)
    final_img = (leaf_rgb * mask_3d + img_np.astype(np.float32) * (1.0 - mask_3d))
    final_img = np.clip(final_img, 0, 255).astype(np.uint8)
    
    final_img = cv2.GaussianBlur(final_img, (3, 3), 0.5)
    return final_img

# Generate pristine sample leaves for testing
if __name__ == "__main__":
    print("Generating sample leaves for each class...")
    for key in DISEASE_DB.keys():
        img = generate_realistic_leaf_image(key, size=(256, 256), seed=42)
        sample_filename = f"sample_{key.lower()}.jpg"
        sample_path = os.path.join(SAMPLES_DIR, sample_filename)
        Image.fromarray(img).save(sample_path, quality=95)
        print(f"Generated sample: {sample_filename}")

    print(f"Successfully generated all {len(DISEASE_DB)} sample leaves in: {SAMPLES_DIR}")

