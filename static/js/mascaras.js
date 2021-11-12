const masks = {
    cpf (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1')
    },
  
    cnpj (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1/$2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1')
    },
  
    phone (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
        .replace(/(-\d{4})\d+?$/, '$1')
    },
  
    phoneDDI (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '+$1 $2')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
        .replace(/(-\d{4})\d+?$/, '$1')
    },
  
    cep (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{5})(\d)/, '$1-$2')
        .replace(/(-\d{3})\d+?$/, '$1')
    },
  
    pis (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{5})(\d)/, '$1.$2')
        .replace(/(\d{5}\.)(\d{2})(\d)/, '$1$2-$3')
        .replace(/(-\d)\d+?$/, '$1')
    },

    percentagem (value) {
      return value
        .replace(/\D+/g, ',')
        .replace(/(\d{4})(\d)/g,"$1,$2")
        .replace(/(,\d{2})\d+?$/, '$1')
    },
    numero (value) {
      return value
        .replace(/\D+/g, '')
        
    },
  
    usuario_e_senha(value) {
      return value
      .replace(/[^\w_]/g, "")

    },

    money (value) {
      const cleanValue = +value.replace(/\D+/g, '')
      const options = { style: 'currency', currency: 'BRL' }
      return new Intl.NumberFormat('pt-br', options).format(cleanValue / 100)
    },
  
    date (value) {
      return value
        .replace('.', '')
    },
  
    dateWithDashes (value) {
      return value
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '$1-$2')
        .replace(/(-\d{2})(\d)/, '$1-$2')
        .replace(/(-\d{4})\d+?$/, '$1')
    },
  }
  
  document.querySelectorAll('input').forEach($input => {
    const field = $input.dataset.js
  
    $input.addEventListener('input', e => {
      e.target.value = masks[field](e.target.value)
    }, false)
  })