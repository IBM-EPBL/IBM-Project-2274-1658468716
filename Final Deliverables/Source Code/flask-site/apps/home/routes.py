# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np

label=['Apple_scab', 
'Apple_Black_rot', 
'Cedar_apple_rust', 
'None', 
'None', 
'Cherry_Powdery_mildew',
'None', 
'Corn_Cercospora_leaf_spot', 
'Corn_Common_rust_', 
'Corn_Northern_Leaf_Blight', 
'None', 
'Grape_Black_rot', 
'Grape_Black_Measles', 
'Grape_Leaf_blight', 
'None', 
'Orange_Haunglongbing', 
'Peach_Bacterial_spot', 
'None', 
'Pepper,_bell_Bacterial_spot', 
'None', 
'Potato_Early_blight', 
'Potato_Late_blight', 
'None', 
'Raspberry_healthy', 
'None', 
'Squash_Powdery_mildew', 
'Strawberry_Leaf_scorch', 
'None', 
'Tomato_Bacterial_spot', 
'Tomato_Early_blight', 
'Tomato_Late_blight', 
'Tomato_Leaf_Mold', 
'Tomato_Septoria_leaf_spot', 
'Tomato_Spider_mites Two-spotted_spider_mite', 
'Tomato_Target_Spot', 
'Tomato_Tomato_Yellow_Leaf_Curl_Virus', 
'Tomato_Tomato_mosaic_virus', 
'None']

desc=["Your apple crop is infected. Spray fungicide – Bonide Captan, wettable sulfur, summer lime sulfur or Spectracide Immunox – when temperatures are above 60 degrees and the leaves or blooms are wet.", 
"Your apple crop is infected. Captan and sulfur products are labeled for control of both scab and black rot. A scab spray program including these chemicals may help prevent the frog-eye leaf spot of black rot, as well as the infection of fruit.",
"Your apple crop is infected. The fungicide myclobutanil (Immunox) is available to homeowners and is effective in controlling apple scab and cedar apple rust.",
"Your apple crop is healthy. 👍", 
"Your blueberry crop is healthy. 👍", 
"Your cherry crop is infected. Apply sulfur or copper-based fungicides to prevent infection of susceptible plants. For best results, apply early or at the first sign of disease. Spray all plant parts thoroughly and repeat at 7-10 day intervals up to the day of harvest.",
"Your cherry crop is healthy. 👍", 
"Your corn crop is infected. Spray whole plant covering leaf, leaf sheath, stalk, ear shoot, as a protective measure, with carbendazim 50% WP @ 2 g or benomyl 50% WP @ 1.5 g/litre of water during first week of July or inception of tassel in disease prone areas where susceptible varieties are grown.", 
"Your corn crop is infected.  Always consider an integrated approach with preventive measures together with biological treatments if available. The application of fungicides can be beneficial when used on susceptible varieties. Apply a foliar fungicide early in the season if rust is bound to spread rapidly due to the weather conditions. Numerous fungicides are available for rust control. Products containing mancozeb, pyraclostrobin, pyraclostrobin + metconazole, pyraclostrobin + fluxapyroxad, azoxystrobin + propiconazole, trifloxystrobin + prothioconazole can be used to control the disease. An example of treatment could be: Spraying of mancozeb @ 2.5 g/l as soon as pustules appear and repeat at 10 days interval till flowering. ",
"Your corn crop is infected.  Foliar fungicides may be applied early in the growing season to corn seedlings as a risk-management tool for northern corn leaf blight and other corn diseases, including anthracnose leaf blight and corn eyespot.", 
"Your corn crop is healthy. 👍", 
"Your grape crop is infected. Mancozeb, and Ziram are all highly effective against black rot. Because these fungicides are strictly protectants, they must be applied before the fungus infects or enters the plant. They protect fruit and foliage by preventing spore germination.",
"Your grape crop is infected. Lime sulfur sprays can manage the trio of pathogens that cause black measles.", 
"Your grape crop is infected. Apply potassium fertilizer in spring or early summer when the vines are just starting to produce Grapes.", 
"Your grape crop is healthy. 👍",
"Your orange crop is infected. Use a citrus fertilizer to prevent this", 
"Your peach crop is infected. Individual leaves with spots can be picked off and destroyed. Compounds available for use on peach and nectarine for bacterial spot include copper, oxytetracycline (Mycoshield and generic equivalents), and syllit+captan; however, repeated applications are typically necessary for even minimal disease control.", 
"Your peach crop is healthy. 👍",
"Your pepper bell crop is infected. Pepper plants require lots of nitrogen during early growth to produce healthy leaves. During the fruiting stage, plants need less nitrogen but plenty of phosphorus and potassium for the best yields. This can be achieved using an even-grade fertilizer all season, or ideally by switching fertilizers halfway through the growing season.", 
"Your pepper bell crop is healthy. 👍", 
"Your potato crop is infected. Early blight can be minimized by maintaining optimum growing conditions, including proper fertilization, irrigation, and management of other pests. Grow later maturing, longer season varieties. Fungicide application is justified only when the disease is initiated early enough to cause economic loss. Eg: AZOXYSTROBIN, BOSCALID",
"Your potato crop is infected. Copper products can effectively control, or slow down, late blight epidemics. Copper products have no kick-back activity. Therefore, they need to be applied to all plant surfaces before infection (before symptoms are observed in the field) and frequently so new foliage is protected as plants grow.", 
"Your potato crop is healthy. 👍", 
"Your raspberry crop is healthy. 👍",
"Your soybean crop is healthy. 👍", 
"Your squash crop is infected. Biological fungicides (such as Serenade) are commercially available beneficial microorganisms formulated into a product that, when sprayed on the plant, destroys fungal pathogens. The active ingredient in Serenade is a bacterium, Bacillus subtilis, that helps prevent the powdery mildew from infecting the plant.", 
"Your strawberry crop is infected. If the plant is on early stage, infected leaves can be removed and disease can be reduced by applying urea",
"Your strawberry crop is healthy. 👍", 
"Your tomato crop is infected. Plant pathogen-free seed or transplants to prevent the introduction of bacterial spot pathogens on contaminated seed or seedlings.  If a clean seed source is not available or you suspect that your seed is contaminated, soak seeds in water at 122°F for 25 min. to kill the pathogens.  To keep leaves dry and to prevent the spread of the pathogens, avoid overhead watering (e.g., with a wand or sprinkler) of established plants and instead use a drip-tape or soaker-hose.", 
"Your tomato crop is infected. Tomatoes that have early blight require immediate attention before the disease takes over the plants. Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate or Bonide Tomato & Vegetable.",
"Your tomato crop is infected. Copper products can effectively control, or slow down, late blight epidemics. Copper products have no kick-back activity. Therefore, they need to be applied to all plant surfaces before infection (before symptoms are observed in the field) and frequently so new foliage is protected as plants grow.", 
"Your tomato crop is infected. Mix 1 tablespoon potassium bicarbonate and ½ teaspoon liquid soap (not detergent) in 1 gallon of water. Spray liberally to all affected areas. This mixture may work better than baking soda as a treatment for existing infections. Or use sulfur-containing organic fungicides as both preventive and treatment for existing infections.", 
"Your tomato crop is infected. An organic fungicide which works against septoria leaf spot is copper fungicide.",
"Your tomato crop is infected. Use abamectin (Agri-Mek SC) at 0.009 to 0.019 lb ai/A. PHI 7 days. REI 12 hr. Retreatment interval 7 days. Do not exceed two sequential applications or 0.056 lb ai/A per season.", 
"Your tomato crop is infected. Products containing chlorothalonil, mancozeb, and copper oxychloride have been shown to provide good control of target spot in research trials. The strobilurin fungicides azoxystrobin and pyraclostrobin, the fungicide boscalid, and the systemic acquired resistance (SAR) elicitor acibenzolar-S-methyl have also been shown to provide good control of target spot.", 
"Your tomato crop is infected. Use a neonicotinoid insecticide, such as dinotefuran (Venom) imidacloprid (AdmirePro, Alias, Nuprid, Widow, and others) or thiamethoxam (Platinum), as a soil application or through the drip irrigation system at transplanting of tomatoes or peppers.",
"Your tomato crop is infected. Remove all infected plants and destroy them. Fungicides won't work against it :(", 
"Your tomato crop is healthy. 👍"]

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/form-upload', methods=['GET', 'POST'])
@login_required
def route_form():
    return render_template('home/form-upload.html', segment='form-upload')

@blueprint.route('/api/upload', methods=['POST'])
@login_required
def upload():
    if request.method == 'POST':
        pic = request.files['image']
        pic_x = pic.filename
        pic.save(pic_x)
        
        cnn = load_model("m1_hdf5.h5")
        dat = load_img(pic_x)
        #dl = tf.reshape(dat, [1,256,256,3])
        test_dat = img_to_array(dat)
        test_dat = test_dat/255.0
        test_dl = np.expand_dims(test_dat, axis=0)
        pred = cnn.predict(test_dl)
        y_class = pred.argmax(axis=1)
        result = label[y_class[0]]
        res1 = desc[y_class[0]]
        return render_template('home/form-upload.html', pred=result, desc=res1)
    return NULL


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
