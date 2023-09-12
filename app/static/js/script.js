window.addEventListener('load', function() 
		{
		  window.location.href = '#';
		});

    

    function copyCode(button) {
      var codeBlock = button.previousElementSibling;
      var codeToCopy = codeBlock.textContent;

      var tempInput = document.createElement("textarea");
      tempInput.value = codeToCopy;
      document.body.appendChild(tempInput);
      tempInput.select();
      document.execCommand("copy");
      document.body.removeChild(tempInput);

      alert("Code copied!");
  }


        
