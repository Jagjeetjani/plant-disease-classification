import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import cv2

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(PROJECT_DIR, "temp_charts")
MODELS_DIR = os.path.join(PROJECT_DIR, "models")
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
SAMPLES_DIR = os.path.join(PROJECT_DIR, "sample_leaves")

os.makedirs(CHARTS_DIR, exist_ok=True)

# Styling palette
PRIMARY_GREEN = "#10B981"
DARK_GREEN = "#065F46"
ACCENT_AMBER = "#F59E0B"
ACCENT_RED = "#EF4444"
BG_DARK = "#0F172A"
TEXT_COLOR = "#F8FAFC"

plt.rcParams.update({
    'font.sans-serif': 'DejaVu Sans',
    'axes.edgecolor': '#334155',
    'axes.linewidth': 1.2,
    'grid.color': '#1E293B',
    'grid.linestyle': '--',
    'grid.alpha': 0.6
})

def generate_all_eda_charts():
    print("Generating comprehensive EDA and diagnostic charts...")
    
    # Load class metadata & database
    db_path = os.path.join(MODELS_DIR, "disease_database.json")
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            disease_db = json.load(f)
    else:
        disease_db = {}

    # 1. CLASS DISTRIBUTION CHART
    fig, ax = plt.subplots(figsize=(12, 6), facecolor="#0F172A")
    ax.set_facecolor("#1E293B")
    
    crops = {}
    for key, data in disease_db.items():
        crop = data.get("crop", "Other")
        crops[crop] = crops.get(crop, 0) + 1
        
    crops_sorted = sorted(crops.items(), key=lambda x: x[1], reverse=True)
    crop_names = [c[0] for c in crops_sorted]
    crop_counts = [c[1] for c in crops_sorted]
    
    bars = ax.bar(crop_names, crop_counts, color=["#10B981", "#3B82F6", "#F59E0B", "#EC4899", "#8B5CF6"], edgecolor="#F8FAFC", linewidth=1.5, width=0.55)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)} Conditions',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color="#F8FAFC")
                    
    ax.set_title("PlantVillage Dataset: Disease Conditions Monitored Per Crop Category", fontsize=14, fontweight='bold', color="#F8FAFC", pad=15)
    ax.set_xlabel("Crop Classification", fontsize=12, fontweight='bold', color="#94A3B8")
    ax.set_ylabel("Number of Diagnosed States", fontsize=12, fontweight='bold', color="#94A3B8")
    ax.tick_params(colors="#94A3B8", labelsize=11)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, "class_distribution.png")
    fig.savefig(chart1_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("Saved:", chart1_path)

    # 2. RGB COLOR DISTRIBUTION: HEALTHY VS DISEASED LEAVES
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0F172A")
    ax1.set_facecolor("#1E293B")
    ax2.set_facecolor("#1E293B")
    
    healthy_sample = os.path.join(SAMPLES_DIR, "sample_tomato___healthy.jpg")
    diseased_sample = os.path.join(SAMPLES_DIR, "sample_tomato___early_blight.jpg")
    
    if os.path.exists(healthy_sample) and os.path.exists(diseased_sample):
        h_img = np.array(Image.open(healthy_sample).convert('RGB'))
        d_img = np.array(Image.open(diseased_sample).convert('RGB'))
        
        colors = ('#EF4444', '#10B981', '#3B82F6')
        color_labels = ('Red Channel', 'Green Channel (Chlorophyll)', 'Blue Channel')
        
        for i, (col, lbl) in enumerate(zip(colors, color_labels)):
            hist_h, bins = np.histogram(h_img[:, :, i], bins=50, range=(0, 256), density=True)
            hist_d, _ = np.histogram(d_img[:, :, i], bins=50, range=(0, 256), density=True)
            bin_centers = (bins[:-1] + bins[1:]) / 2
            ax1.plot(bin_centers, hist_h, color=col, label=lbl, linewidth=2.2)
            ax2.plot(bin_centers, hist_d, color=col, label=lbl, linewidth=2.2)
            
        ax1.set_title("Healthy Tomato Leaf: High Green Peak (Chlorophyll Saturation)", fontsize=11, fontweight='bold', color="#10B981")
        ax1.set_xlabel("Pixel Intensity (0 - 255)", fontsize=10, color="#94A3B8")
        ax1.set_ylabel("Pixel Density", fontsize=10, color="#94A3B8")
        ax1.tick_params(colors="#94A3B8")
        ax1.legend(loc='upper right', facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC")
        ax1.grid(alpha=0.3)
        
        ax2.set_title("Early Blight Leaf: Shift Toward Red/Necrotic Pigmentation", fontsize=11, fontweight='bold', color="#EF4444")
        ax2.set_xlabel("Pixel Intensity (0 - 255)", fontsize=10, color="#94A3B8")
        ax2.tick_params(colors="#94A3B8")
        ax2.legend(loc='upper right', facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC")
        ax2.grid(alpha=0.3)
        
    plt.suptitle("RGB Spectral Profile Comparison: Chlorophyll Green vs Necrotic Lesions", fontsize=13, fontweight='bold', color="#F8FAFC", y=1.02)
    plt.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, "rgb_color_distribution.png")
    fig.savefig(chart2_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("Saved:", chart2_path)

    # 3. HSV COLOR SPACE DENSITY (HUE MAPPING)
    fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0F172A")
    ax.set_facecolor("#1E293B")
    
    if os.path.exists(healthy_sample) and os.path.exists(diseased_sample):
        h_hsv = cv2.cvtColor(h_img, cv2.COLOR_RGB2HSV)
        d_hsv = cv2.cvtColor(d_img, cv2.COLOR_RGB2HSV)
        
        hue_h, bins = np.histogram(h_hsv[:, :, 0], bins=60, range=(0, 180), density=True)
        hue_d, _ = np.histogram(d_hsv[:, :, 0], bins=60, range=(0, 180), density=True)
        bin_c = (bins[:-1] + bins[1:]) / 2
        
        ax.plot(bin_c, hue_h, color="#10B981", label="Healthy Foliage (Strong Green Band ~35-75°)", linewidth=2.5)
        ax.fill_between(bin_c, 0, hue_h, color="#10B981", alpha=0.25)
        
        ax.plot(bin_c, hue_d, color="#F59E0B", label="Diseased Foliage (Chlorosis & Necrosis Band ~10-30°)", linewidth=2.5)
        ax.fill_between(bin_c, 0, hue_d, color="#F59E0B", alpha=0.25)
        
        ax.set_title("HSV Hue Spectral Distribution: Detecting Chlorotic Yellowing & Necrosis", fontsize=13, fontweight='bold', color="#F8FAFC", pad=12)
        ax.set_xlabel("Hue Angle (Degrees in OpenCV [0-180])", fontsize=11, color="#94A3B8")
        ax.set_ylabel("Relative Pixel Frequency", fontsize=11, color="#94A3B8")
        ax.tick_params(colors="#94A3B8")
        ax.legend(facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC", loc='upper right')
        ax.grid(alpha=0.3)
        
    plt.tight_layout()
    chart3_path = os.path.join(CHARTS_DIR, "hsv_color_space.png")
    fig.savefig(chart3_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("Saved:", chart3_path)

    # 4. DATA AUGMENTATION PIPELINE VISUALIZATION
    if os.path.exists(healthy_sample):
        orig_img = Image.open(healthy_sample).resize((128, 128))
        orig_np = np.array(orig_img)
        
        fig, axes = plt.subplots(1, 5, figsize=(15, 3.5), facecolor="#0F172A")
        aug_titles = ["Original", "Random Rotation (90°)", "Horizontal Flip", "Zoom / Crop", "Brightness Shift"]
        
        # Augmentations
        a1 = orig_np
        a2 = np.rot90(orig_np, 1)
        a3 = np.fliplr(orig_np)
        h_crop, w_crop = 100, 100
        crop = orig_np[14:114, 14:114]
        a4 = cv2.resize(crop, (128, 128))
        a5 = np.clip(orig_np * 1.35, 0, 255).astype(np.uint8)
        
        augs = [a1, a2, a3, a4, a5]
        for ax, img, title in zip(axes, augs, aug_titles):
            ax.set_facecolor("#1E293B")
            ax.imshow(img)
            ax.set_title(title, fontsize=10, fontweight='bold', color="#F8FAFC")
            ax.axis('off')
            
        plt.suptitle("Deep Learning Data Augmentation Pipeline: Enhancing Generalization in Field Imagery", fontsize=13, fontweight='bold', color="#10B981", y=1.05)
        plt.tight_layout()
        chart4_path = os.path.join(CHARTS_DIR, "augmentation_pipeline.png")
        fig.savefig(chart4_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        print("Saved:", chart4_path)

    # 5. MODEL BENCHMARKS (CNN vs Transfer Learning)
    metrics_path = os.path.join(MODELS_DIR, "model_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
        cnn_data = metrics["models"]["Custom_CNN"]
        mob_data = metrics["models"]["Transfer_MobileNetV2"]
        
        # Bar comparison
        fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0F172A")
        ax.set_facecolor("#1E293B")
        
        categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        cnn_scores = [cnn_data['accuracy'] * 100, cnn_data['precision'] * 100, cnn_data['recall'] * 100, cnn_data['f1_score'] * 100]
        mob_scores = [mob_data['accuracy'] * 100, mob_data['precision'] * 100, mob_data['recall'] * 100, mob_data['f1_score'] * 100]
        
        x = np.arange(len(categories))
        width = 0.35
        
        rects1 = ax.bar(x - width/2, cnn_scores, width, label='Custom Deep CNN (Scratch)', color='#3B82F6', edgecolor="#F8FAFC", linewidth=1.2)
        rects2 = ax.bar(x + width/2, mob_scores, width, label='Transfer Learning (MobileNetV2)', color='#10B981', edgecolor="#F8FAFC", linewidth=1.2)
        
        for rect in rects1:
            h = rect.get_height()
            ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#93C5FD")
                        
        for rect in rects2:
            h = rect.get_height()
            ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold', color="#6EE7B7")
                        
        ax.set_title("Performance Comparison: Custom CNN vs Transfer Learning MobileNetV2", fontsize=13, fontweight='bold', color="#F8FAFC", pad=15)
        ax.set_ylabel("Score (%)", fontsize=11, color="#94A3B8")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=11, fontweight='bold', color="#F8FAFC")
        ax.set_ylim(0, 115)
        ax.tick_params(colors="#94A3B8")
        ax.legend(facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC", loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        chart5_path = os.path.join(CHARTS_DIR, "model_accuracy_comparison.png")
        fig.savefig(chart5_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        print("Saved:", chart5_path)

        # 6. TRAINING & VALIDATION LOSS/ACCURACY CURVES
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), facecolor="#0F172A")
        ax1.set_facecolor("#1E293B")
        ax2.set_facecolor("#1E293B")
        
        cnn_epochs = range(1, len(cnn_data['train_history']['accuracy']) + 1)
        mob_epochs = range(1, len(mob_data['train_history']['accuracy']) + 1)
        
        # Accuracy curves
        ax1.plot(cnn_epochs, [v * 100 for v in cnn_data['train_history']['accuracy']], color="#3B82F6", linestyle="--", label="CNN Train Acc")
        ax1.plot(cnn_epochs, [v * 100 for v in cnn_data['train_history']['val_accuracy']], color="#60A5FA", linewidth=2.2, label="CNN Val Acc")
        ax1.plot(mob_epochs, [v * 100 for v in mob_data['train_history']['accuracy']], color="#059669", linestyle="--", label="MobileNetV2 Train Acc")
        ax1.plot(mob_epochs, [v * 100 for v in mob_data['train_history']['val_accuracy']], color="#10B981", linewidth=2.2, label="MobileNetV2 Val Acc")
        
        ax1.set_title("Training & Validation Accuracy Across Epochs", fontsize=11, fontweight='bold', color="#F8FAFC")
        ax1.set_xlabel("Epochs", fontsize=10, color="#94A3B8")
        ax1.set_ylabel("Accuracy (%)", fontsize=10, color="#94A3B8")
        ax1.tick_params(colors="#94A3B8")
        ax1.legend(facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=9)
        ax1.grid(alpha=0.3)
        
        # Loss curves
        ax2.plot(cnn_epochs, cnn_data['train_history']['loss'], color="#3B82F6", linestyle="--", label="CNN Train Loss")
        ax2.plot(cnn_epochs, cnn_data['train_history']['val_loss'], color="#60A5FA", linewidth=2.2, label="CNN Val Loss")
        ax2.plot(mob_epochs, mob_data['train_history']['loss'], color="#059669", linestyle="--", label="MobileNetV2 Train Loss")
        ax2.plot(mob_epochs, mob_data['train_history']['val_loss'], color="#10B981", linewidth=2.2, label="MobileNetV2 Val Loss")
        
        ax2.set_title("Categorical Cross-Entropy Loss Convergence", fontsize=11, fontweight='bold', color="#F8FAFC")
        ax2.set_xlabel("Epochs", fontsize=10, color="#94A3B8")
        ax2.set_ylabel("Cross-Entropy Loss", fontsize=10, color="#94A3B8")
        ax2.tick_params(colors="#94A3B8")
        ax2.legend(facecolor="#0F172A", edgecolor="#334155", labelcolor="#F8FAFC", fontsize=9)
        ax2.grid(alpha=0.3)
        
        plt.suptitle("Model Learning Dynamics & Generalization Convergence", fontsize=13, fontweight='bold', color="#10B981", y=1.02)
        plt.tight_layout()
        chart6_path = os.path.join(CHARTS_DIR, "loss_accuracy_curves.png")
        fig.savefig(chart6_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        print("Saved:", chart6_path)

        # 6B. CONFUSION MATRIX HEATMAP (CNN)
        fig, ax = plt.subplots(figsize=(11, 9), facecolor="#0F172A")
        ax.set_facecolor("#1E293B")
        cm_cnn = np.array(cnn_data['confusion_matrix'])
        class_short = [c.replace("___", "\n").replace("_", " ") for c in metrics["dataset_info"]["classes"]]
        
        sns.heatmap(cm_cnn, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=class_short, yticklabels=class_short,
                    cbar_kws={'label': 'Sample Count'}, linewidths=0.5, linecolor="#0F172A")
                    
        ax.set_title(f"Custom Deep CNN Confusion Matrix (Overall Accuracy: {cnn_data['accuracy']*100:.1f}%)",
                     fontsize=13, fontweight='bold', color="#F8FAFC", pad=15)
        ax.set_xlabel("Predicted Class", fontsize=11, fontweight='bold', color="#94A3B8")
        ax.set_ylabel("True Ground Truth Class", fontsize=11, fontweight='bold', color="#94A3B8")
        ax.tick_params(colors="#94A3B8", labelsize=8)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        chart6b_path = os.path.join(CHARTS_DIR, "confusion_matrix_cnn.png")
        fig.savefig(chart6b_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        print("Saved:", chart6b_path)


        # 7. CONFUSION MATRIX HEATMAP (MobileNetV2)
        fig, ax = plt.subplots(figsize=(11, 9), facecolor="#0F172A")
        ax.set_facecolor("#1E293B")
        
        cm = np.array(mob_data['confusion_matrix'])
        class_short = [c.replace("___", "\n").replace("_", " ") for c in metrics["dataset_info"]["classes"]]
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', ax=ax,
                    xticklabels=class_short, yticklabels=class_short,
                    cbar_kws={'label': 'Sample Count'}, linewidths=0.5, linecolor="#0F172A")
                    
        ax.set_title(f"MobileNetV2 Confusion Matrix (Overall Accuracy: {mob_data['accuracy']*100:.1f}%)",
                     fontsize=13, fontweight='bold', color="#F8FAFC", pad=15)
        ax.set_xlabel("Predicted Class", fontsize=11, fontweight='bold', color="#94A3B8")
        ax.set_ylabel("True Ground Truth Class", fontsize=11, fontweight='bold', color="#94A3B8")
        ax.tick_params(colors="#94A3B8", labelsize=8)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        chart7_path = os.path.join(CHARTS_DIR, "confusion_matrix_transfer.png")
        fig.savefig(chart7_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
        plt.close(fig)
        print("Saved:", chart7_path)

    # 8. DISEASE SEVERITY MATRIX
    fig, ax = plt.subplots(figsize=(11, 6), facecolor="#0F172A")
    ax.set_facecolor("#1E293B")
    
    pathogens = {"Fungus": 0, "Oomycete": 0, "Virus": 0, "Bacterium": 0, "Healthy (None)": 0}
    for item in disease_db.values():
        p_raw = item.get("pathogen", "Other")
        if "Fungus" in p_raw:
            pathogens["Fungus"] += 1
        elif "Oomycete" in p_raw:
            pathogens["Oomycete"] += 1
        elif "Virus" in p_raw:
            pathogens["Virus"] += 1
        elif "Bacter" in p_raw:
            pathogens["Bacterium"] += 1
        else:
            pathogens["Healthy (None)"] += 1
            
    p_names = list(pathogens.keys())
    p_counts = list(pathogens.values())
    colors_pie = ["#EF4444", "#F59E0B", "#8B5CF6", "#3B82F6", "#10B981"]
    
    wedges, texts, autotexts = ax.pie(
        p_counts, labels=p_names, autopct='%1.1f%%',
        colors=colors_pie, startangle=140,
        textprops=dict(color="#F8FAFC", fontweight='bold'),
        wedgeprops=dict(edgecolor="#0F172A", linewidth=2, width=0.6)
    )
    for at in autotexts:
        at.set_color("#FFFFFF")
        at.set_fontsize(10)
        
    ax.set_title("Pathogen Etiology Breakdown Across Evaluated Plant Diseases", fontsize=13, fontweight='bold', color="#F8FAFC", pad=20)
    plt.tight_layout()
    chart8_path = os.path.join(CHARTS_DIR, "disease_pathogen_breakdown.png")
    fig.savefig(chart8_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close(fig)
    print("Saved:", chart8_path)

    print("All EDA and diagnostic charts successfully created in:", CHARTS_DIR)

if __name__ == "__main__":
    generate_all_eda_charts()
