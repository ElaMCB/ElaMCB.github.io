#!/usr/bin/env python
"""
Bio-AI Analogies: Educational Content Generator
This script generates educational content that explains AI concepts using biological analogies.
It can be integrated with the BDH model for inference or run independently.
"""

import argparse
import random
import json
import os
from typing import Dict, List, Tuple

# Dictionary of AI concepts and their biological analogies
AI_BIO_ANALOGIES = {
    "neural_networks": {
        "concept": "Neural Networks",
        "analogies": [
            {
                "title": "Brain Neurons and Artificial Neurons",
                "explanation": "Just as the brain consists of interconnected neurons that process and transmit information, artificial neural networks consist of nodes (artificial neurons) that process inputs and transmit outputs to other nodes. Both systems learn by strengthening connections between neurons based on experience.",
                "example": "When you touch something hot, sensory neurons send signals to processing neurons, which activate motor neurons to pull your hand away. Similarly, in a neural network, input nodes detect patterns, hidden nodes process this information, and output nodes produce a response."
            },
            {
                "title": "Learning as Synaptic Plasticity",
                "explanation": "The brain learns by adjusting the strength of connections (synapses) between neurons, a process called synaptic plasticity. Neural networks learn by adjusting weights between artificial neurons through backpropagation, which is analogous to how synaptic connections strengthen or weaken based on experience.",
                "example": "When you practice playing piano, the neural connections involved in that skill strengthen. Similarly, when a neural network is trained to recognize cats, the connections that lead to correct cat identification are strengthened."
            }
        ]
    },
    "attention_mechanisms": {
        "concept": "Attention Mechanisms",
        "analogies": [
            {
                "title": "Selective Attention in Vision",
                "explanation": "Humans can focus on specific objects in their visual field while ignoring others - like spotting a friend in a crowd. Similarly, attention mechanisms in AI allow models to focus on relevant parts of the input data while processing less important parts with less intensity.",
                "example": "When reading a book, you focus on specific words while being peripherally aware of the surrounding text. Transformer models like GPT use attention to focus on relevant words when generating the next word in a sequence."
            },
            {
                "title": "Cocktail Party Effect",
                "explanation": "Humans can focus on a single conversation in a noisy room (the cocktail party effect). This is similar to how attention mechanisms in AI can filter out noise and focus on relevant signals in data.",
                "example": "At a party, you can focus on your friend's voice despite many conversations happening. Similarly, in speech recognition, attention helps the model focus on the speaker's voice while filtering out background noise."
            }
        ]
    },
    "reinforcement_learning": {
        "concept": "Reinforcement Learning",
        "analogies": [
            {
                "title": "Animal Training and Rewards",
                "explanation": "Animals learn behaviors through positive reinforcement (rewards) and negative reinforcement (avoiding punishment). Similarly, reinforcement learning algorithms learn optimal behaviors by maximizing rewards and minimizing penalties in their environment.",
                "example": "A dog learns to sit when given treats after sitting. Similarly, an RL agent playing chess receives positive rewards for good moves and negative rewards for bad ones, gradually learning optimal strategies."
            },
            {
                "title": "Foraging Behavior",
                "explanation": "Animals must balance exploring new food sources (exploration) with returning to known food sources (exploitation). Reinforcement learning algorithms face the same exploration-exploitation dilemma when deciding whether to try new actions or stick with known successful actions.",
                "example": "Bees scout for new flower patches while also returning to known productive patches. Similarly, a reinforcement learning algorithm playing a game must balance trying new strategies with using proven successful ones."
            }
        ]
    },
    "generative_models": {
        "concept": "Generative Models",
        "analogies": [
            {
                "title": "Imagination and Dreams",
                "explanation": "The human brain can generate new images, scenarios, and ideas through imagination and dreams, combining and transforming existing memories and concepts. Similarly, generative AI models like GANs and diffusion models can create new content by learning patterns from existing data.",
                "example": "When you dream, your brain creates new scenarios from memories and experiences. Similarly, a generative model trained on images of dogs can create new, never-before-seen dog images by learning the patterns that make up 'dog-ness'."
            },
            {
                "title": "Genetic Recombination",
                "explanation": "In sexual reproduction, genetic material from two parents combines to create offspring with new genetic combinations. Similarly, some generative models combine features from different inputs to generate new outputs that blend characteristics of the originals.",
                "example": "A child inherits a mix of traits from both parents, creating a unique individual. Similarly, style transfer in AI can combine the content of one image with the artistic style of another to create something new."
            }
        ]
    },
    "bounded_depth_hierarchy": {
        "concept": "Bounded Depth Hierarchy (BDH)",
        "analogies": [
            {
                "title": "Hierarchical Processing in Visual Cortex",
                "explanation": "The visual cortex processes information in a hierarchy, with early layers detecting simple features like edges and later layers recognizing complex objects. Similarly, the BDH model processes information through a bounded hierarchy of layers, each building on the previous one's representations.",
                "example": "When you see a face, your visual system first detects edges and contours, then combines these into features like eyes and noses, and finally recognizes the whole face. BDH similarly builds up from simple patterns to complex representations, but with a carefully bounded depth to maintain efficiency."
            },
            {
                "title": "Ecological Pyramids",
                "explanation": "In ecosystems, energy flows through trophic levels in a pyramid structure, with each level supporting the next. Similarly, in BDH, information flows through a bounded number of hierarchical levels, with each level transforming and refining the representations from the previous level.",
                "example": "In an ecosystem, plants capture energy from the sun, herbivores eat plants, and carnivores eat herbivores, with energy transferring up the pyramid but diminishing at each level. In BDH, information similarly flows through a pyramid-like structure, with each level extracting higher-level patterns from the previous level's output."
            }
        ]
    }
}

def get_random_analogy(concept: str = None) -> Dict:
    """
    Get a random analogy for a specific AI concept or a random concept if none specified.
    
    Args:
        concept: The AI concept to get an analogy for (optional)
        
    Returns:
        A dictionary containing the analogy information
    """
    if concept and concept in AI_BIO_ANALOGIES:
        concept_data = AI_BIO_ANALOGIES[concept]
        analogy = random.choice(concept_data["analogies"])
        return {
            "concept": concept_data["concept"],
            "title": analogy["title"],
            "explanation": analogy["explanation"],
            "example": analogy["example"]
        }
    else:
        # Choose a random concept
        concept_key = random.choice(list(AI_BIO_ANALOGIES.keys()))
        concept_data = AI_BIO_ANALOGIES[concept_key]
        analogy = random.choice(concept_data["analogies"])
        return {
            "concept": concept_data["concept"],
            "title": analogy["title"],
            "explanation": analogy["explanation"],
            "example": analogy["example"]
        }

def generate_educational_content(prompt: str = None, concept: str = None) -> str:
    """
    Generate educational content based on a prompt or concept.
    
    Args:
        prompt: A text prompt to guide the content generation (optional)
        concept: A specific AI concept to explain (optional)
        
    Returns:
        A formatted educational content string
    """
    # If a specific concept is requested, use that
    if concept:
        analogy = get_random_analogy(concept)
    # Otherwise, try to extract a concept from the prompt or choose randomly
    elif prompt:
        # Simple keyword matching to find relevant concepts
        for key in AI_BIO_ANALOGIES:
            if key.replace("_", " ") in prompt.lower() or AI_BIO_ANALOGIES[key]["concept"].lower() in prompt.lower():
                analogy = get_random_analogy(key)
                break
        else:
            # No matching concept found, choose randomly
            analogy = get_random_analogy()
    else:
        # No prompt or concept, choose randomly
        analogy = get_random_analogy()
    
    # Format the educational content
    content = f"""
# {analogy['concept']}: {analogy['title']}

## The Biological Analogy

{analogy['explanation']}

## Real-World Example

{analogy['example']}

---
*This educational content was generated by the Bio-AI Analogies tool, powered by the Baby Dragon Hatchling (BDH) model.*
"""
    return content

def list_available_concepts() -> None:
    """Print all available AI concepts that have biological analogies."""
    print("\nAvailable AI Concepts with Biological Analogies:")
    print("------------------------------------------------")
    for key, value in AI_BIO_ANALOGIES.items():
        print(f"- {value['concept']} ({key})")
    print("\n")

def main():
    """Main function to run the script from command line."""
    parser = argparse.ArgumentParser(description="Generate educational content explaining AI concepts using biological analogies")
    parser.add_argument("--prompt", type=str, help="A text prompt to guide the content generation")
    parser.add_argument("--concept", type=str, help="A specific AI concept to explain")
    parser.add_argument("--list", action="store_true", help="List all available AI concepts")
    parser.add_argument("--output", type=str, help="Output file to save the generated content (optional)")
    
    args = parser.parse_args()
    
    if args.list:
        list_available_concepts()
        return
    
    content = generate_educational_content(args.prompt, args.concept)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(content)
        print(f"Educational content saved to {args.output}")
    else:
        print(content)

if __name__ == "__main__":
    main()