PREFIX=smart_nanopore_10

EXE_PRE=/home/genomika25/miniconda3/envs/genomika/bin/wtpre
EXE_ZMO=/home/genomika25/miniconda3/envs/genomika/bin/wtzmo
EXE_OBT=/home/genomika25/miniconda3/envs/genomika/bin/wtobt
EXE_GBO=/home/genomika25/miniconda3/envs/genomika/bin/wtgbo
EXE_CLP=/home/genomika25/miniconda3/envs/genomika/bin/wtclp
EXE_LAY=/home/genomika25/miniconda3/envs/genomika/bin/wtlay
EXE_CNS=/home/genomika25/miniconda3/envs/genomika/bin/wtcns
N_THREADS=8

all:$(PREFIX).dmo.cns

$(PREFIX).fa.gz:
	$(EXE_PRE) -J 5000 nanopore_clean_10.fq | gzip -c -1 > $@

$(PREFIX).dmo.ovl:$(PREFIX).fa.gz
	$(EXE_ZMO) -t $(N_THREADS) -i $(PREFIX).fa.gz -fo $@ -k 16 -z 10 -Z 16 -U -1 -m 0.1 -A 1000

$(PREFIX).dmo.obt:$(PREFIX).fa.gz $(PREFIX).dmo.ovl
	$(EXE_CLP) -i $(PREFIX).dmo.ovl -fo $@ -d 3 -k 300 -m 0.1 -FT

$(PREFIX).dmo.lay:$(PREFIX).fa.gz $(PREFIX).dmo.obt $(PREFIX).dmo.ovl
	$(EXE_LAY) -i $(PREFIX).fa.gz -b $(PREFIX).dmo.obt -j $(PREFIX).dmo.ovl -fo $(PREFIX).dmo.lay -w 300 -s 200 -m 0.1 -r 0.95 -c 1

$(PREFIX).dmo.cns:$(PREFIX).dmo.lay
	$(EXE_CNS) -t $(N_THREADS) $< > $@ 2> $@.log

