# 🤖 LLM Finetuning Dataset Generator

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> An automated tool for generating high-quality outputs for LLM finetuning datasets using API Key based model APIs.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dataset Format](#-dataset-format)
- [Directory Structure](#-directory-structure)
- [How It Works](#-how-it-works)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

## 🌟 Overview

The **LLM Finetuning Dataset Generator** is a powerful automation tool designed to streamline the process of generating output responses for machine learning datasets. It leverages API Key based model APIs to generate high-quality outputs based on your custom system prompts.

### Key Highlights

✨ **Smart Skip Feature** - Automatically skips rows that already have outputs  
⚡ **High Performance** - Generate approximately 500+ rows per run  
🎯 **Custom Prompts** - Support for custom system prompts  
🔄 **Batch Processing** - Process multiple dataset files simultaneously

## 🚀 Features

- 🤖 **Automated Output Generation** - Generate responses using advanced LLM models
- 📊 **Batch Processing** - Handle multiple dataset files in one go
- 🔍 **Intelligent Skipping** - Skip rows with existing outputs automatically
- ⚙️ **Custom System Prompts** - Use your own system prompts for generation
- 📈 **Scalable** - Generates ~430K rows per day with Nvidia Free API Key on a single device
- 💻 **Multiple Devices Compatible** - Also works in Pydroid3 Mobile Application
- 💾 **JSON Support** - Works with standard JSON dataset format

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/sujalrajpoot/LLM-Finetuning-Dataset-Generator.git
cd LLM-Finetuning-Dataset-Generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your dataset files**
   - Place all dataset files in the `Dataset-Files/` directory
   - Ensure they follow the required JSON format (see below)

## 🎯 Usage

1. **Prepare your datasets** in the required JSON format
2. **Place them** in the `Dataset-Files/` folder
3. **Run the generator**:
    ```bash
    python concurrently_main.py
    ```

The tool will automatically:
- Process all JSON files in the directory
- Generate outputs for empty fields
- Skip rows with existing outputs
- Save the updated datasets

## 📝 Dataset Format

Your dataset files must follow this exact JSON structure:

```json
[
    {
        "instruction": "Summarize the given text into one sentence.",
        "input": "Artificial Intelligence is transforming industries by automating tasks, enhancing decision-making, and improving user experiences across sectors like healthcare, finance, and education.",
        "output": ""
    },
    {
        "instruction": "Translate the following English sentence into French.",
        "input": "The weather is beautiful today.",
        "output": ""
    },
    {
        "instruction": "Write a Python function that reverses a string.",
        "input": "",
        "output": ""
    },
    {
        "instruction": "Generate three creative business name ideas for a coffee shop.",
        "input": "",
        "output": ""
    },
    {
        "instruction": "Classify the sentiment of the given text as Positive, Negative, or Neutral.",
        "input": "I really love the new phone update; it runs faster and looks amazing!",
        "output": ""
    },
    {
        "instruction": "Write a short poem about the sunset.",
        "input": "",
        "output": ""
    },
    {
        "instruction": "Explain the concept of machine learning in simple terms.",
        "input": "",
        "output": ""
    },
    {
        "instruction": "Convert the following temperature from Celsius to Fahrenheit.",
        "input": "25°C",
        "output": ""
    },
    {
        "instruction": "Write a SQL query to select all users who registered in the last 30 days.",
        "input": "",
        "output": ""
    },
    {
        "instruction": "Create a short ad copy for an eco-friendly water bottle brand.",
        "input": "",
        "output": ""
    }
]
```

### Required Fields

| Field | Description | Required |
|-------|-------------|----------|
| `instruction` | The task or prompt for the model | ✅ Yes |
| `input` | The input data/context | ✅ Optional — Yes if the task depends on context|
| `output` | The generated response (leave empty for generation) | ✅ Yes |

## 📁 Directory Structure
```
📁 LLM-Finetuning-Dataset-Generator/
├── 📁 Config/
│   └── 📄 config.py
├── 📁 Providers/
│   ├── 📄 DeepInfra.py
│   ├── 📄 Nvidia.py
│   └── 📄 __init__.py
├── 📁 dataset_files/
|   ├── 📄 dataset_1.json
│   └── 📄 dataset_2.json
├── 📄 requirements.txt
└── 📄 main.py
```

## ⚙️ How It Works

1. 📂 **File Detection** - Scans the `Dataset-Files/` directory for JSON files
2. 🔍 **Row Analysis** - Checks each row for empty output fields
3. 🤖 **API Communication** - Uses API Key based model APIs with custom system prompts
4. ✍️ **Output Generation** - Generates high-quality responses for empty fields
5. ⏭️ **Smart Skipping** - Automatically skips rows with existing outputs
6. 💾 **Auto-Save** - Saves updated datasets with generated outputs

## 🔮 Future Improvements

We're constantly working to make this tool better! Here's what's on the roadmap:

- [ ] 🌐 **More LLM Providers** - Add support for additional free LLM model providers
- [ ] 📊 **Enhanced Scalability** - Improve dataset generation capacity for large datasets
- [ ] 🛠️ **Better Error Handling** - Implement advanced troubleshooting features
- [ ] 📈 **Progress Tracking** - Add real-time progress bars and statistics
- [ ] 🔧 **Configuration File** - Support for external configuration files
- [ ] 🎨 **GUI Interface** - Optional graphical user interface
- [ ] 📝 **Logging System** - Comprehensive logging for debugging

## 🤝 Contributing

Contributions are welcome! This is an open-source project aimed at improving dataset generation efficiency.

### How to Contribute

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💻 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 Open a Pull Request

### Contribution Guidelines

- Write clean, documented code
- Test your changes thoroughly
- Update documentation as needed
- Follow existing code style
- Be respectful and constructive

## ⚠️ Disclaimer

**This tool is intended for educational purposes only** - to automate the dataset generation process and enhance productivity in machine learning workflows.

- 📚 **Educational Use** - Designed for learning and research
- 🚫 **No Malicious Intent** - Not intended to harm any API or organization
- ⚖️ **Responsible Use** - Users are responsible for compliance with API terms of service
- 🔒 **Respect Rate Limits** - Use responsibly and respect API rate limits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who help improve this tool
- Inspired by the need for efficient dataset preparation in ML/AI workflows
- Built with ❤️ for the open-source community

## 📧 Contact

Have questions or suggestions? Feel free to:
- 🐛 Open an issue
- 💬 Start a discussion
- ⭐ Star the repository if you find it useful!

---

<div align="center">
Developed by: Sujal Rajpoot
🎯 Full Stack Python Developer & AI Fine-Tuning Expert
🚀 Founder of TrueSyncAI — Custom AI Solutions for Everyone

**Made with ❤️ for the ML/AI Community**

⭐ Star this repository if you find it helpful!
</div>