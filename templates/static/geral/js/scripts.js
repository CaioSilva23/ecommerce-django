(function () {
    select_variacao = document.getElementById('select-variacoes');
    variation_preco = document.getElementById('variation-preco');
    variation_preco_promocional = document.getElementById('variation-preco-promocional');

    if (!select_variacao) {
        return;
    }

    if (!variation_preco) {
        return;
    }

    select_variacao.addEventListener('change', function () {
        preco = this.options[this.selectedIndex].getAttribute('data-preco');
        preco_promocional = this.options[this.selectedIndex].getAttribute('data-preco-promocional');

        variation_preco.innerHTML = preco;

        if (variation_preco_promocional) {
            variation_preco_promocional.innerHTML = preco_promocional;
        }
    })
})();



const cep = document.querySelector("#id_cep")
const rua = document.querySelector("#id_rua")
const bairro = document.querySelector("#id_bairro")
const cidade = document.querySelector("#id_cidade")
const complemento = document.querySelector("#id_complemento")
const uf = document.querySelector("#id_estado")


cep.addEventListener('focusout',async () => {

    const onlyNumbers = /^[0-9]+$/;
    const cepValid = /^[0-9]{8}$/;

    if (!onlyNumbers.test(cep.value) || !cepValid.test(cep.value)){
        swal('Opss !', "Cep inválido!")
    }

  const response = await fetch(`https://viacep.com.br/ws/${cep.value}/json/`); 

  if (!response.ok){
    swal('Opss !', 'Cep não encontrado, tente novamente!')
  }

  const responseCep = await response.json()
  rua.value = responseCep.logradouro;
  bairro.value = responseCep.bairro;
  cidade.value = responseCep.localidade;
  complemento.value = responseCep.complemento;
  uf.value = responseCep.uf;
  
})