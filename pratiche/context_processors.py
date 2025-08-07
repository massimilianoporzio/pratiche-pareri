

def project_context(request):
    """
    Context processor to add project-related information to the context.
    """
    context = {
                'project_name': 'Pratiche e Pareri',
                'project_version': '1.0.0',
                'project_description': 'This is a sample project for demonstration purposes.',
                'email_sviluppatore': 'massimiliano.porzio@gmail.com'
    }
    return context