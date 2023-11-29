import base64
import tenseal as ts 
import pandas as pd

# reading data from excel sheet
data = pd.read_excel('salary.xlsx')
salary = data['Salary'].tolist()
# there are 26 values in this list

######################################################
#############methods to saving txt files##############
######################################################
def write_data(file_name: str, data: bytes):
    data = base64.b64encode(data)
    
    with open(file_name, 'wb') as f:
        f.write(data)
def read_data(file_name: str) -> bytes:
    with open(file_name, "rb") as f:
        data = f.read()
    return base64.b64decode(data)

# generating keys and serializing 'context'
context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes = [60, 40, 40, 60]
)

# We are saving the keys here
context.generate_galois_keys()
context.global_scale = 2**40    # the higher the value the more secure

# secret.txt saves the secret key
secret_context = context.serialize(save_secret_key = True)
write_data("secret.txt", secret_context)

# droopping the public key
context.make_context_public()
public_context = context.serialize()
write_data("public.txt", public_context)



# ENCRYPTING
context = ts.context_from(read_data("secret.txt"))
salary_encrypted = ts.ckks_vector(context, salary)
write_data("salary_encrypted.txt", salary_encrypted.serialize())

contexts = ts.context_from(read_data("public.txt"))
salary_proto = read_data("salary_encrypted.txt")
encrypted = ts.lazy_ckks_vector_from(salary_proto)
encrypted.link_context(contexts)


"""
    CALCULATIONS
    Here we have data operators on the salary_data without having to decrypt
"""
average = sum(salary) / len(salary)
encrypt_average = ts.ckks_vector(context, [average])
write_data("average_salary_encrypted.txt", encrypt_average.serialize())

# decrypting here
ave_proto = read_data("average_salary_encrypted.txt")
ave = ts.lazy_ckks_vector_from(ave_proto)
ave.link_context(context)
z = ave.decrypt()[0]
print(z)


########################################
########################################
# THIS IS USING ENCRYPTED WAGE INCREASES
########################################
########################################

wage_increase = [1.2]
encrypted_wage_increase = ts.ckks_vector(context, wage_increase)
bonus_increase = [500]
encrypted_bonus_increase = ts.ckks_vector(context, bonus_increase)
write_data("weighted_wageweight.txt", encrypted_wage_increase.serialize())
write_data("weighted_bonusweight.txt", encrypted_bonus_increase.serialize())


# CALCULATIONS using encrypted-encrypted vectors
w_proto = read_data("weighted_wageweight.txt")
w = ts.lazy_ckks_vector_from(w_proto)
w.link_context(context)

b_proto = read_data("weighted_bonusweight.txt")
b = ts.lazy_ckks_vector_from(b_proto)
b.link_context(context)

new2 = salary_encrypted * w + b
write_data("salary_encrypted_with_vectors.txt", new2.serialize())

# DECRYPTION from encryption-encrypted vectors
m2_proto = read_data("salary_encrypted_with_vectors.txt")
m2 = ts.lazy_ckks_vector_from(m2_proto)
m2.link_context(context)
y = []
for i in range(len(m2.decrypt()[:])):
    y.append(round(m2.decrypt()[i], 0))

print(y)
