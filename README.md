## 🌐 Ver Blogs Generados

You can view the generated blogs directly on [GitHub Pages](https://alejandroors21.github.io/blogger-agent-tfg/).

## Daggr Workflow

```mermaid
graph TD;
    style_analyzer --> keyword_extractor --> content_generator --> critic --> refinement --> html_builder --> image_selector;

    %% Adding Icons/Emojis for each phase
    style_analyzer["📏 Style Analyzer"];
    keyword_extractor["🔍 Keyword Extractor"];
    content_generator["✍️ Content Generator"];
    critic["🤔 Critic"];
    refinement["✍️ Refinement"];
    html_builder["🖥️ HTML Builder"];
    image_selector["🖼️ Image Selector"];
```

This flowchart illustrates the data flow between the various agents involved in the Daggr workflow.