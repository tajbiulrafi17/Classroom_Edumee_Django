const emailField=document.querySelector('#emailField');
const feedbackArea=document.querySelector(".invalid-feedback");

emailField.addEventListener("keyup", (e) =>{

    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid');
    feedbackArea.style.display = "none";

    if(emailVal.length > 0){
        fetch("/validate-email/",{
            body:JSON.stringify({'email': emailVal}),
            method: "POST",
        }).then(res=>res.json()).then(data=>{
            console.log("data", data);
            if(data.email_error){
                emailField.classList.add('is-invalid');
                feedbackArea.style.display = "block";
                feedbackArea.innerHTML=`<p>${data.email_error}</p>`
            }
        })
    }
        
});