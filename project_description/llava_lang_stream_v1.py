import streamlit as st
import base64
import json
from typing import Dict, Any, Optional
from PIL import Image
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
import io


class ImageAnalyzer:
    """Analyzes images using Ollama's LLaVA model with LangChain."""
    
    QUESTIONS = {
        "categoria": "what type of category is this?",
        "identificadores": "what tags or identification numbers are visible?",
        "origen": "what location or origin text is visible?",
        "condicion": "describe the health and body condition",
        "atributos": "what are the key characteristics?",
        "resumen": "describe this image in detail"
    }
    
    def __init__(self, model: str = "llava", base_url: str = "http://localhost:11434"):
        """Initialize the analyzer with LangChain ChatOllama model.
        
        Args:
            model: Name of the Ollama model to use
            base_url: Base URL for Ollama API
        """
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0
        )
    
    def encode_image(self, image_source) -> str:
        """Encode image to base64 string.
        
        Args:
            image_source: PIL Image or file path
            
        Returns:
            Base64 encoded image string
        """
        if isinstance(image_source, str):
            img = Image.open(image_source)
        else:
            img = image_source
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def create_prompt(self) -> str:
        """Create structured prompt from questions dictionary.
        
        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "Analyze this image and answer the following questions in JSON format.",
            "Return ONLY a valid JSON object with these keys:\n"
        ]
        
        for key, question in self.QUESTIONS.items():
            prompt_parts.append(f'- "{key}": {question}')
        
        prompt_parts.append("\nRespond in Spanish. Return only the JSON object, no additional text.")
        
        return "\n".join(prompt_parts)
    
    def analyze(self, image_source) -> Dict[str, Any]:
        """Analyze an image and return structured results.
        
        Args:
            image_source: PIL Image or file path
            
        Returns:
            Dictionary with analysis results
            
        Raises:
            RuntimeError: If analysis fails
        """
        image_base64 = self.encode_image(image_source)
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": self.create_prompt()},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{image_base64}"
                }
            ]
        )
        
        response = self.llm.invoke([message])
        result = self._parse_response(response.content)
        return result
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate JSON response.
        
        Args:
            response_text: Raw response text from model
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            RuntimeError: If JSON parsing fails
        """
        text = response_text.strip()
        
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
            text = text.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON response: {e}\nResponse: {text}")


def render_sidebar() -> tuple[str, str]:
    """Render sidebar configuration options.
    
    Returns:
        Tuple of (model_name, base_url)
    """
    with st.sidebar:
        st.header("Configuration")
        
        model_name = st.selectbox(
            "Model Selection",
            ["llava", "llava:13b", "llava:34b"],
            index=0,
            help="Choose the LLaVA model variant"
        )
        
        base_url = st.text_input(
            "Ollama Base URL",
            value="http://localhost:11434",
            help="URL where Ollama is running"
        )
        
        st.divider()
        
        st.subheader("Analysis Fields")
        st.json({
            "categoria": "Product category",
            "identificadores": "Tags/IDs visible",
            "origen": "Location/origin text",
            "condicion": "Health/condition",
            "atributos": "Key characteristics",
            "resumen": "Detailed description"
        })
        
        st.divider()
        
        st.subheader("System Requirements")
        st.code("ollama pull llava", language="bash")
        st.markdown("[Download Ollama](https://ollama.ai)")
        
    return model_name, base_url


def render_upload_section() -> Optional[Image.Image]:
    """Render image upload section.
    
    Returns:
        PIL Image if uploaded, None otherwise
    """
    st.subheader("Image Upload")
    
    uploaded_file = st.file_uploader(
        "Select an image file",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, JPEG, PNG, WEBP"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=None)
        return image
    
    return None


def render_results_section(result: Dict[str, Any]) -> None:
    """Render analysis results section.
    
    Args:
        result: Analysis result dictionary
    """
    st.subheader("Analysis Results")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Structured View", "JSON View"])
    
    with tab1:
        # Display each field in a clean card-like format
        fields = [
            ("Categoría", "categoria"),
            ("Identificadores", "identificadores"),
            ("Origen", "origen"),
            ("Condición", "condicion"),
            ("Atributos", "atributos"),
            ("Resumen", "resumen")
        ]
        
        for label, key in fields:
            with st.container():
                st.markdown(f"**{label}**")
                value = result.get(key, "N/A")
                
                # Handle different types of values
                if isinstance(value, (list, dict)):
                    st.json(value)
                else:
                    st.write(value)
                st.divider()
    
    with tab2:
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        st.code(json_str, language="json")
        
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="analysis_result.json",
            mime="application/json"
        )


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Image Analysis System",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("Image Analysis System")
    st.markdown("Automated image analysis using LLaVA vision model with structured output generation.")
    
    # Render sidebar and get configuration
    model_name, base_url = render_sidebar()
    
    # Main content area with two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Upload section
        image = render_upload_section()
        
        if image is not None:
            analyze_button = st.button(
                "Analyze Image",
                type="primary"
            )
            
            if analyze_button:
                with st.spinner("Processing image analysis..."):
                    try:
                        analyzer = ImageAnalyzer(model=model_name, base_url=base_url)
                        result = analyzer.analyze(image)
                        
                        st.session_state['analysis_result'] = result
                        st.session_state['analyzed'] = True
                        
                        st.success("Analysis completed successfully")
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")
                        
                        if "model 'llava' not found" in str(e).lower():
                            st.info("Solution: Execute 'ollama pull llava' in your terminal")
    
    with col2:
        # Results section
        if st.session_state.get('analyzed', False) and 'analysis_result' in st.session_state:
            render_results_section(st.session_state['analysis_result'])
        else:
            st.info("Upload an image and click 'Analyze Image' to view results")
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Powered by Ollama LLaVA | LangChain | Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    # Initialize session state
    if 'analyzed' not in st.session_state:
        st.session_state['analyzed'] = False
    
    main()