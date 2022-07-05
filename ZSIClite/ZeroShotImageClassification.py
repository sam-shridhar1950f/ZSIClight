from typing import List, Union
import clip 
import PIL 
from PIL import Image
import os
import torch 
from torch import Tensor
import scipy 

print("Eureka!")
class ZeroShotImageClassification():


  def __init__(self, 
               *args, 
               **kwargs):
    
         """
          Load CLIP models based on either language needs or vision backbone needs
          With english labelling users have the liberty to choose different vision backbones
          Multi-lingual labelling is only supported with ViT as vision backbone.
          Args:
              Model (`str`, *optional*, defaults to `ViT-B/32`):
                Any one of the CNN or Transformer based pretrained models can be used as Vision backbone. 
                `RN50`, `RN101`, `RN50x4`, `RN50x16`, `RN50x64`, `ViT-B/32`, `ViT-B/16`, `ViT-L/14`
              Lang (`str`, *optional*, defaults to `en`):
                Any one of the language codes below
                ar, bg, ca, cs, da, de, el, es, et, fa, fi, fr, fr-ca, gl, gu, he, hi, hr, hu, 
                hy, id, it, ja, ka, ko, ku, lt, lv, mk, mn, mr, ms, my, nb, nl, pl, pt, pt, pt-br, 
                ro, ru, sk, sl, sq, sr, sv, th, tr, uk, ur, vi, zh-cn, zh-tw.   
         """
    
         if "lang" in kwargs:
            self.lang = kwargs["lang"]
         else:
            self.lang = "en"

         lang_codes = self.available_languages()

         if self.lang not in lang_codes:
            raise Exception('Language code {} not valid, supported codes are {} '.format(self.lang, lang_codes))
            return 

         device = "cpu" 

         if self.lang == "en":
            model_tag = "ViT-B/32"
            if "model" in kwargs:
                model_tag = kwargs["model"] 
            print("Loading OpenAI CLIP model {} ...".format(model_tag))    
            self.model, self.preprocess = clip.load(model_tag, device=device) 
            print("Label language {} ...".format(self.lang))
         else:          
            raise("only en is currently supported.")

  def available_models(self):
      """Returns the names of available CLIP models"""
      return clip.available_models()

  def available_languages(self):
      """Returns the codes of available languages"""
      codes = """ar, bg, ca, cs, da, de, en, el, es, et, fa, fi, fr, fr-ca, gl, gu, he, hi, hr, hu, 
      hy, id, it, ja, ka, ko, ku, lt, lv, mk, mn, mr, ms, my, nb, nl, pl, pt, pt, pt-br, 
      ro, ru, sk, sl, sq, sr, sv, th, tr, uk, ur, vi, zh-cn, zh-tw"""
      return set([code.strip() for code in codes.split(",")])
  def cos_sim(a: Tensor, b: Tensor):
   
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))



  def _load_image(self, image: str) -> "PIL.Image.Image":
      """
      Loads `image` to a PIL Image.
      Args:
          image (`str` ):
              The image to convert to the PIL Image format.
      Returns:
          `PIL.Image.Image`: A PIL Image.
      """
      if isinstance(image, str):
          
          if os.path.isfile(image):
              image = PIL.Image.open(image)
          else:
              raise ValueError(
                  f"Incorrect path or url, URLs must start with `http://` or `https://`, and {image} is not a valid path"
              )
      elif isinstance(image, PIL.Image.Image):
          image = image
      else:
          raise ValueError(
              "Incorrect format used for image. Should be an url linking to an image, a local path, or a PIL image."
          )
      image = PIL.ImageOps.exif_transpose(image)
      image = image.convert("RGB")
      return image            

  def __call__(
        self, 
        image: str,
        candidate_labels: Union[str, List[str]],
        *args,
        **kwargs,
    ):

        """
        Classify the image using the candidate labels given
        Args:
            image (`str`):
                Fully Qualified path of a local image or URL of image
            candidate_labels (`str` or `List[str]`):
                The set of possible class labels to classify each sequence into. Can be a single label, a string of
                comma-separated labels, or a list of labels.
            hypothesis_template (`str`, *optional*, defaults to `"A photo of {}."`, if lang is default / `en`):
                The template used to turn each label into a string. This template must include a {} or
                similar syntax for the candidate label to be inserted into the template. 
            top_k (`int`, *optional*, defaults to 5):
                The number of top labels that will be returned by the pipeline. If the provided number is higher than
                the number of labels available in the model configuration, it will default to the number of labels.
        Return:
            A `dict` or a list of `dict`: Each result comes as a dictionary with the following keys:
            - **image** (`str`) -- The image for which this is the output.
            - **labels** (`List[str]`) -- The labels sorted by order of likelihood.
            - **scores** (`List[float]`) -- The probabilities for each of the labels.
        """

        device = "cpu"

        if self.lang == "en":
            if "hypothesis_template" in kwargs:
                hypothesis_template = kwargs["hypothesis_template"] 
            else:
                hypothesis_template = "A photo of {}"

            if isinstance(candidate_labels, str):
              labels = [hypothesis_template.format(candidate_label) for candidate_label in candidate_labels.split(",")]
            else:    
              labels = [hypothesis_template.format(candidate_label) for candidate_label in candidate_labels]
        else:
            if "hypothesis_template" in kwargs:
                hypothesis_template = kwargs["hypothesis_template"] 
            else:
                hypothesis_template = "{}"

            if isinstance(candidate_labels, str):
              labels = [hypothesis_template.format(candidate_label) for candidate_label in candidate_labels.split(",")]
            else:    
              labels = [hypothesis_template.format(candidate_label) for candidate_label in candidate_labels]

        # TO BE IMPLEMENTED  
        if  "top_k" in kwargs:
             top_k = kwargs["top_k"] 
        else:
             top_k = len(labels)
        

        if str(type(self.model)) == "<class 'clip.model.CLIP'>":
            img = self.preprocess(self._load_image(image)).unsqueeze(0).to(device)
            text = clip.tokenize(labels).to(device)
            image_features = self.model.encode_image(img)
            image_features = image_features.detach().numpy()
            text_features = self.model.encode_text(text)
            #text_features = text_features.detach().numpy()
            
            #image_features = image_features.ravel()
            #text_features = text_features.ravel()
            #print(image_features)
            #print(text_features)
        else:    
            #image_features = torch.tensor(self.model.encode(self._load_image(image)))
            #text_features = torch.tensor(self.text_model.encode(labels))
            print("F")
        
        sim_scores = cos_sim(text_features, image_features)
        #simwab = scipy.spatial.distance.cosine(text_features, image_features)
        #print(sim_scores)
        #print(simwab)
        out = []
        for sim_score in sim_scores:
            out.append(sim_score.item() * 100)
        probs = [[out]]
       # probs = probs.softmax(dim=-1).cpu().numpy()
        probs = scipy.special.softmax(probs)
        scores = list(probs.flatten())
        
        sorted_sl = sorted(zip(scores, candidate_labels), key=lambda t:t[0], reverse=True)  
        scores, candidate_labels = zip(*sorted_sl)
        
        preds = {}
        preds["image"] = image
        preds["scores"] = scores
        preds["labels"] = candidate_labels
        return preds
