f = open("web-queues/education_profiles.wq", "r")
f1 = open("web-queues/education_profiles_1.wq", "w")
lines = f.readlines()
url = "https://www.ohio.edu/education/faculty-and-staff/"

for line in lines:
    f1.write(url + line)
