//to be integrated
retrieveStore = ()=>{
	let results  = localStorage.getItem("gn_markdown_editabable")

	return results? results: ""
}

updateStore = (data)=>{
	localStorage.setItem("gn_markdown_editabable",data)
}

cleanStore = ()=>{
	localStorage.setItem("gn_markdown_editabable","")
}