import { getRepositoryDetails } from "../../utils";

export interface Project {
  name: string;
  demoLink: string;
  tags?: string[],
  description?: string;
  postLink?: string;
  demoLinkRel?: string;
  [key: string]: any;
}

export const projects: Project[] = [
  {
    name: 'Age Prediction App',
    description: 'Lets you predict the ages from photos using AI.',
    demoLink: 'https://github.com/bniladridas/age-pred',
    tags: ['AI', 'Machine Learning']
  },
  {
    name: 'Churn Prediction Challenge for Video Streaming Service',
    description: 'Predicting customer churn for a video streaming service.',
    demoLink: 'https://github.com/bniladridas/ChurnPrediction',
    demoLinkRel: 'nofollow noopener noreferrer',
    tags: ['Data Science', 'Machine Learning']
  },
  {
    name: 'DeepVision: Cutting-Edge Image Classification with TensorFlow & Keras',
    description: 'CIFAR-10 Image Classification with MobileNetV2',
    demoLink: 'https://github.com/bniladridas/deepvision',
    demoLinkRel: 'nofollow noopener noreferrer',
    tags: ['AI', 'Deep Learning']
  },
  {
    ...(await getRepositoryDetails('bniladridas/facerecognition')),
    name: 'Face Recognition with OpenCV and face_recognition',
    demoLink: 'https://github.com/bniladridas/facerecognition',
    postLink: 'https://niladridas.hashnode.dev/how-to-detect-and-track-objects-in-real-time-with-a-macbook-camera',
    tags: ['AI', 'Computer Vision']
  },
  {
    ...(await getRepositoryDetails('bniladridas/imageclassification')),
    name: 'Image Classification with InceptionV3',
    demoLink: 'https://github.com/bniladridas/imageclassification',
    tags: ['AI', 'Deep Learning']
  },
  {
    ...(await getRepositoryDetails('bniladridas/voice-assistant-chatbot')),
    name: 'Voice Assistant Chatbot',
    demoLink: 'https://github.com/bniladridas/voice-assistant-chatbot',
    tags: ['AI', 'Natural Language Processing']
  },
  {
    ...(await getRepositoryDetails('bniladridas/gan')),
    name: 'GAN Image Generation',
    demoLink: 'https://github.com/bniladridas/gan',
    tags: ['AI', 'Generative Adversarial Networks']
  },
  {
    ...(await getRepositoryDetails('bniladridas/movieml')),
    name: 'Hybrid Movie Recommendation System: The Ultimate Personalized Movie Experience',
    demoLink: 'https://github.com/bniladridas/movieml',
    tags: ['AI', 'Recommendation Systems']
  }
]
