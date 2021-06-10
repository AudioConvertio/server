function handleFiles(files){
    const elem = document.getElementById("select_files");
    elem.innerHTML = (files.length === 1) ? 'Um arquivo Selecionado' : `${files.length} arquivos selecionados`;
}