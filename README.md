# MetAssembly

MetAssembly is a workflow for assembly of metagenomics data.
It provides as end results both the assembled contigs as well as
evaluation reports of said assembly.

MetAssembly is a workflow composed of:

- [MEGAHIT](https://github.com/voutcn/megahit) for assembly of input reads
- [Quast](https://github.com/ablab/quast), specifically MetaQuast, for assembly evaluation.

---

### References

Li, D., Luo, R., Liu, C.M., Leung, C.M., Ting, H.F., Sadakane, K., Yamashita, H. and Lam, T.W., 2016. MEGAHIT v1.0: A Fast and Scalable Metagenome Assembler driven by Advanced Methodologies and Community Practices. Methods.

Alla Mikheenko, Vladislav Saveliev, Alexey Gurevich,
MetaQUAST: evaluation of metagenome assemblies,
Bioinformatics (2016) 32 (7): 1088-1090. doi: 10.1093/bioinformatics/btv697
