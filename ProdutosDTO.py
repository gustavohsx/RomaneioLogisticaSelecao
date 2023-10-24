class ProdutosDTO:

    def __init__(self, codigo_fabrica, ean, ean_tributavel, ncm, cest, cfop, descricao, unidade, quantidade, codigo_barras, v_un_com, v_prod, u_trib, q_trib, v_un_trib, ind_tot):
        self._codigo_fabrica = codigo_fabrica
        self._ean = ean
        self._ean_tributavel = ean_tributavel
        self._ncm = ncm
        self._cest = cest
        self._cfop = cfop
        self._descricao = descricao
        self._unidade = unidade
        self._quantidade = quantidade
        self._codigo_barras = codigo_barras
        self._v_un_com = v_un_com
        self._v_prod = v_prod
        self._u_trib = u_trib
        self._q_trib = q_trib
        self._v_un_trib = v_un_trib
        self._ind_tot = ind_tot

    # Getters
    def get_codigo_fabrica(self):
        return self._codigo_fabrica

    def get_ean(self):
        return self._ean

    def get_ean_tributavel(self):
        return self._ean_tributavel

    def get_ncm(self):
        return self._ncm

    def get_cest(self):
        return self._cest

    def get_cfop(self):
        return self._cfop

    def get_descricao(self):
        return self._descricao

    def get_unidade(self):
        return self._unidade

    def get_quantidade(self):
        return self._quantidade

    def get_codigo_barras(self):
        return self._codigo_barras

    def get_v_un_com(self):
        return self._v_un_com

    def get_v_prod(self):
        return self._v_prod

    def get_u_trib(self):
        return self._u_trib

    def get_q_trib(self):
        return self._q_trib

    def get_v_un_trib(self):
        return self._v_un_trib

    def get_ind_tot(self):
        return self._ind_tot

    # Setters
    def set_codigo_fabrica(self, codigo_fabrica):
        self._codigo_fabrica = codigo_fabrica

    def set_ean(self, ean):
        self._ean = ean

    def set_ean_tributavel(self, ean_tributavel):
        self._ean_tributavel = ean_tributavel

    def set_ncm(self, ncm):
        self._ncm = ncm

    def set_cest(self, cest):
        self._cest = cest

    def set_cfop(self, cfop):
        self._cfop = cfop

    def set_descricao(self, descricao):
        self._descricao = descricao

    def set_unidade(self, unidade):
        self._unidade = unidade

    def set_quantidade(self, quantidade):
        self._quantidade = quantidade

    def set_codigo_barras(self, codigo_barras):
        self._codigo_barras = codigo_barras

    def set_v_un_com(self, v_un_com):
        self._v_un_com = v_un_com

    def set_v_prod(self, v_prod):
        self._v_prod = v_prod

    def set_u_trib(self, u_trib):
        self._u_trib = u_trib

    def set_q_trib(self, q_trib):
        self._q_trib = q_trib

    def set_v_un_trib(self, v_un_trib):
        self._v_un_trib = v_un_trib

    def set_ind_tot(self, ind_tot):
        self._ind_tot = ind_tot

    def __str__(self) -> str:
        return f'{self._codigo_fabrica} - {self._descricao} - {self._quantidade}{self._unidade} - {self._codigo_barras}'
    