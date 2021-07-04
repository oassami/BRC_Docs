var deleteModal = document.getElementById('deleteModal')
deleteModal.addEventListener('show.bs.modal', function (event) {
var button = event.relatedTarget
var delete_name = button.getAttribute('data-bs-name')
var delete_id = button.getAttribute('data-bs-id')
var modalBodyText = deleteModal.querySelector('.modal-body-text')
var modalURL = deleteModal.querySelector('#delete_id')
modalBodyText.textContent = 'Are you sure you want to delete (' + delete_name + ')'
modalURL.href = '/brc/user/delete/' + delete_id
})