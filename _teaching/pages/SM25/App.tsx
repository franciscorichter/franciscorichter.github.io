import './App.css';
import { Card } from './components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { FileIcon, BookOpen, GraduationCap, BookMarked, Users } from 'lucide-react';

function App() {

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <header className="bg-gradient-to-r from-indigo-700 to-purple-800 text-white py-12 px-6 shadow-lg">
        <div className="container mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Stochastic Methods</h1>
          <div className="flex flex-col md:flex-row md:items-center text-lg opacity-90">
            <div className="flex items-center mr-6 mb-2 md:mb-0">
              <GraduationCap className="mr-2" />
              <span>Università della Svizzera italiana, Faculty of Informatics</span>
            </div>
            <div className="flex items-center">
              <BookMarked className="mr-2" />
              <span>Spring 2025</span>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <Card className="p-6 mb-8 shadow-md">
            <p className="text-lg leading-relaxed mb-4">
              This course covers foundational and advanced topics in <strong>stochastic processes</strong>, focusing on both theoretical principles and practical applications. Students learn to <strong>model randomness in systems, analyze probabilistic phenomena, and apply stochastic methods</strong> in various domains, including <strong>optimization, inference, networks, and simulation</strong>.
            </p>
          </Card>

          <Tabs defaultValue="overview" className="mb-12">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="overview">Course Overview</TabsTrigger>
              <TabsTrigger value="objectives">Learning Objectives</TabsTrigger>
              <TabsTrigger value="references">References</TabsTrigger>
            </TabsList>
            
            <TabsContent value="overview" className="mt-6">
              <h2 className="text-2xl font-bold mb-6 text-indigo-800">Course Overview</h2>
              <p className="mb-6 text-lg">
                The course covers a <strong>broad range of stochastic techniques</strong>, structured into <strong>thirteen main topics</strong>, each with corresponding <strong>lecture notes</strong>:
              </p>

              <div className="space-y-8">
                {/* Lecture 1 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">1. Randomness</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week1.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 1: Randomness
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Random number generators (RNGs) and their properties</li>
                    <li>Pseudorandom number generation: Linear Congruential Generators (LCG), PCG64</li>
                    <li>Probability distributions: uniform, discrete, continuous</li>
                    <li>Inverse transform sampling</li>
                  </ul>
                </div>

                {/* Lecture 2 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">2. Random Variables</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week2.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 2: Random Variables
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Discrete vs. continuous random variables</li>
                    <li>Probability mass functions (PMF) and probability density functions (PDF)</li>
                    <li>Cumulative distribution functions (CDF) and their properties</li>
                    <li>Binomial, Poisson, and normal distributions</li>
                  </ul>
                </div>

                {/* Lecture 3 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">3. Expectation & Limit Theorems</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week3.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 3: Expectation
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Definition of expectation and its properties</li>
                    <li>Linearity of expectation</li>
                    <li>The <strong>Law of Large Numbers (LLN)</strong></li>
                    <li>The <strong>Central Limit Theorem (CLT)</strong> and its implications</li>
                    <li>Monte Carlo simulation for numerical approximations</li>
                  </ul>
                </div>

                {/* Lecture 4 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">4. Variance & Monte Carlo Methods</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week4.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 4: Variance
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Monte Carlo integration and importance sampling</li>
                    <li>Variance reduction techniques (stratified sampling, control variates, antithetic variates)</li>
                    <li>Rejection sampling and proof of correctness</li>
                    <li>Dependence and independence of random variables</li>
                    <li>Bayesian inference and Bayes' theorem</li>
                  </ul>
                </div>

                {/* Lecture 5 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">5. Networks & Random Graphs</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week5.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 5: Networks
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Introduction to <strong>random networks</strong></li>
                    <li>Graph theory: adjacency matrices and connectivity</li>
                    <li>Erdős–Rényi random graphs</li>
                    <li>Structural Equation Models (SEM) and causality in networks</li>
                    <li>Applications in epidemiology and network analysis</li>
                  </ul>
                </div>

                {/* Lecture 6 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">6. Markov Processes</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week6.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 6: Markov Processes
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li><strong>Markov chains</strong>: transition matrices, Chapman-Kolmogorov equation</li>
                    <li>Random walks and applications in financial models</li>
                    <li>Stationary distributions and <strong>ergodicity</strong></li>
                    <li>Multi-step transition probabilities and long-term behavior</li>
                    <li>Applications in <strong>epidemiology and finance</strong></li>
                  </ul>
                </div>

                {/* Lecture 7 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">7. Stochastic Simulation</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week7.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 7: Stochastic Simulation
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li>Stochastic Cellular Automata and probabilistic grid-based models</li>
                    <li>Agent-Based Modeling (ABM) and emergent behavior</li>
                    <li>Example: <strong>Forest fire model</strong> (spread of wildfire simulation)</li>
                    <li>Example: <strong>Ant foraging simulation</strong> (pheromone-based search strategies)</li>
                  </ul>
                </div>

                {/* Lecture 8 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">8. Stochastic Inference</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week8.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 8: Stochastic Inference
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li><strong>Linear Regression</strong> and least squares estimation</li>
                    <li><strong>Logistic Regression</strong> and Maximum Likelihood Estimation (MLE)</li>
                    <li><strong>Support Vector Machines (SVMs)</strong> for classification</li>
                    <li><strong>Neural networks</strong> and stochastic optimization methods</li>
                  </ul>
                </div>

                {/* Lecture 9 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">9. Stochastic Optimization</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week9.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 9: Stochastic Optimization
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li><strong>Evolutionary algorithms</strong>: Genetic algorithms (GA) & Differential Evolution (DE)</li>
                    <li><strong>Stochastic Gradient Descent (SGD)</strong> and its variants</li>
                    <li><strong>ADAM optimizer</strong>: adaptive learning rates for optimization</li>
                    <li><strong>Expectation-Maximization (EM) algorithm</strong> and Monte Carlo EM</li>
                    <li><strong>Markov Chain Monte Carlo (MCMC)</strong> methods</li>
                  </ul>
                </div>

                {/* Lecture 10 */}
                <div className="bg-white rounded-lg shadow-md p-6 transition-all hover:shadow-lg">
                  <h3 className="text-xl font-bold text-indigo-700 mb-3">10. Stochastic Systems & Multi-Agent Models</h3>
                  <div className="flex items-center mb-4">
                    <FileIcon className="mr-2 text-indigo-600" size={18} />
                    <a 
                      href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/_teaching/Notes/week10.pdf" 
                      className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium"
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      Lecture 10: Stochastic Systems
                    </a>
                  </div>
                  <ul className="list-disc pl-5 space-y-1 text-gray-700">
                    <li><strong>Multi-agent stochastic systems</strong>: Defining agents, tasks, tools, and processes</li>
                    <li><strong>Markov Decision Processes (MDP)</strong></li>
         
(Content truncated due to size limit. Use line ranges to read in chunks)