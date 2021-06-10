function handleFiles(files){
    const elem = document.getElementById("select_files");
    const err = document.getElementById("error_message");
    elem.innerHTML = (files.length === 1) ? 'Um arquivo Selecionado' : `${files.length} arquivos selecionados`;
    if(err !== null){
        err.remove()
    }
}