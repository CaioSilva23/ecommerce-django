

function validaCpf(strCpf) {
    if (!/[0-9]{11}/.test(strCpf)) return false;
    if (strCpf === "00000000000") return false;

    var soma = 0;

    for (var i = 1; i <= 9; i++) {
        soma += parseInt(strCpf.substring(i - 1, i)) * (11 - i);
    }

    var resto = soma % 11;

    if (resto === 10 || resto === 11 || resto < 2) {
        resto = 0;
    } else {
        resto = 11 - resto;
    }

    if (resto !== parseInt(strCpf.substring(9, 10))) {
        console.log('inválido')
        return false;
    }

    soma = 0;

    for (var i = 1; i <= 10; i++) {
        soma += parseInt(strCpf.substring(i - 1, i)) * (12 - i);
    }
    resto = soma % 11;

    if (resto === 10 || resto === 11 || resto < 2) {
        resto = 0;
    } else {
        resto = 11 - resto;
    }
 
    if (resto !== parseInt(strCpf.substring(10, 11))) {
        console.log('inválido')
        return false;
    }

    return strCpf;
}


const cpf  = document.querySelector("#id_cpf").value.replace('.', '').replace('.','').replace('-','')


if (validaCpf(cpf)){
    if(cpf){
     
        $("#id_cpf").attr('disabled', 'disabled');
        return cpf
    };
};




