project.py runs on a window sub-linux environment with tenSEAL to make the homomorphic encryption project. 

We parse the salary data in the excel sheet to find calculate the mean salary of all the employees in the encrypted data so that nobody's salary can be known. 

As homomorphic encryption takes a long time and generates a large key size, we found that it really wouldn't be beneficial at all to encrypt the workers' names.

Files such as secret.txt and public.txt are private and public keys, respectively, to allow users to encrypt and decrypt data. The private key must be kept a secret so that those who are not authorized should not have access to the results after the computations were performed on the encrypted data. 

We can see that files such as new_salary.txt and average_salary_encrypted.txt contain illegible letters, as it's encrypted. The mathematical steps are done in this encrypted data, which is what the point of HE was. 

In the terminal, we can see that the average is actually the same as the actual data before and after the computations. 

Real application: 
Having created the public and the private key, a real-application that may use HE is any organization that may want to collaborate on data analytics without sharing sensitive information such as individual's salaries. It is important to recognize that one's salary is a very sensitive information and should be private.

https://github.com/OpenMined/TenSEAL

