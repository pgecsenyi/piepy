from string import Template

class DeltaTemplate(Template):

    delimiter = "%"

def strfdelta(tdelta, fmt):

    data = {"D": tdelta.days}
    data["H"], rem = divmod(tdelta.seconds, 3600)
    data["M"], data["S"] = divmod(rem, 60)
    template = DeltaTemplate(fmt)

    return template.substitute(data)
