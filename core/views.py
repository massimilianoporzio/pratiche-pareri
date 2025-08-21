def error_500_test(request):
    """
    Questa vista genera un errore 500 per testare la pagina custom.
    """
    raise ValueError("Questo è un errore di test per la pagina 500.")
