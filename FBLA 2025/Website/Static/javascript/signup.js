
document.addEventListener('DOMContentLoaded', function() {
  const ownerRadio = document.getElementById('owner');
  const customerRadio = document.getElementById('customer');
  const businessField = document.getElementById('business-name-field');

  function toggleBusinessField() {
    if (ownerRadio.checked) {
      businessField.style.display = 'block';
      document.getElementById('BusinessName').required = true;
    } else {
      businessField.style.display = 'none';
      document.getElementById('BusinessName').required = false;
    }
  }

  ownerRadio.addEventListener('change', toggleBusinessField);
  customerRadio.addEventListener('change', toggleBusinessField);
});