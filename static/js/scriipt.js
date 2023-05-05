var answerResult

function changeBtnName()  {
    const btnElement 
      = document.getElementById('btn');
    
    btnElement.value = "새이름!";
  }

  function printName()  {
    const name = document.getElementById('name').value;
    document.getElementById("result").innerText = name;  
    answerResult = name
    console.log(answerResult)
  }