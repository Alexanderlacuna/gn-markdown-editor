//parse for converting markdown to html



 function  configureMarkdownParser() { 
 	//add code highlighting functionality
   const {markedHighlight} = globalThis.markedHighlight;
   let new_marked = new marked.Marked(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : 'plaintext';
      return hljs.highlight(code, { language }).value;
    }
  })
)
     // Set options
  new_marked.use({
    pedantic: false,
    gfm: true,
  });


   return new_marked
}

function updatePreview(){
   previewContent = document.querySelector("#output");
  var markdownContent = editor.getValue();
  var htmlContent = configureMarkdownParser().parse(markdownContent)
  previewContent.innerHTML = htmlContent;
}


