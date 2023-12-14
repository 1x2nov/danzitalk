from django.db import models

class Reality(models.Model):
    kaptCode = models.CharField(max_length=16, null=True, db_index=True)
    secondName = models.CharField(max_length=51, null=True)

    bjdCode = models.CharField(max_length=11, null=True)
    codeAptNm = models.CharField(max_length=51, null=True)
    codeGarbage = models.CharField(max_length=16, null=True)
    codeHallNm = models.CharField(max_length=51, null=True)
    codeHeatNm = models.CharField(max_length=51, null=True)
    codeMgrNm = models.CharField(max_length=51, null=True)
    codeNet = models.CharField(max_length=6, null=True)
    codeSaleNm = models.CharField(max_length=51, null=True)
    codeStr = models.CharField(max_length=16, null=True)
    convenientFacility = models.CharField(max_length=501, null=True)
    doroJuso = models.CharField(max_length=366, null=True)
    educationFacility = models.CharField(max_length=501, null=True)
    hoCnt = models.PositiveIntegerField(null=True)
    kaptAcompany = models.CharField(max_length=101, null=True)
    kaptAddr = models.CharField(max_length=201, null=True)
    kaptBcompany = models.CharField(max_length=101, null=True)
    kaptdaCnt = models.PositiveIntegerField(null=True)
    kaptdCccnt = models.PositiveIntegerField(null=True)
    kaptdEcnt = models.PositiveIntegerField(null=True)
    kaptDongCnt = models.PositiveIntegerField(null=True)
    kaptdPcnt = models.PositiveIntegerField(default=0)
    kaptdPcntu = models.PositiveIntegerField(default=0)
    kaptdWtimebus = models.CharField(max_length=11, null=True)
    kaptdWtimesub = models.CharField(max_length=11, null=True)
    kaptFax = models.CharField(max_length=21, null=True)
    kaptMarea = models.FloatField(default=0.0)
    kaptMparea_135 = models.PositiveIntegerField(null=True)
    kaptMparea_136 = models.PositiveIntegerField(null=True)
    kaptMparea_60 = models.PositiveIntegerField(null=True)
    kaptMparea_85 = models.PositiveIntegerField(null=True)
    kaptName = models.CharField(max_length=51, null=True)
    kaptTarea = models.FloatField(default=0.0)
    kaptTel = models.CharField(max_length=21, null=True)
    kaptUrl = models.CharField(max_length=101, null=True)
    kaptUsedate = models.CharField(max_length=9, null=True)
    privArea = models.FloatField(default=0.0)
    subwayLine = models.CharField(max_length=51, null=True)
    subwayStation = models.CharField(max_length=51, null=True)
    welfareFacility = models.CharField(max_length=201, null=True)

    bun = models.PositiveIntegerField(null=True)
    ji = models.PositiveIntegerField(null=True)

    mgmBldrgstPk = models.CharField(max_length=34, null=True)
    platArea = models.FloatField(default=0.0)
    archArea = models.FloatField(default=0.0)
    bcRat = models.FloatField(default=0.0)
    totArea = models.FloatField(default=0.0)
    vlRatEstmTotArea = models.FloatField(default=0.0)
    vlRat = models.FloatField(default=0.0)
    hhldCnt = models.PositiveIntegerField(null=True)
    engrGrade = models.CharField(max_length=5, null=True)

    amount = models.CharField(max_length=41, null=True)
    useArea = models.FloatField(default=0.0)

    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)

    hits = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'Reality'

class Bookmark(models.Model):
    user = models.ForeignKey("community.User", on_delete=models.CASCADE, related_name='bookmarks')
    reality = models.ForeignKey('Reality', on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        db_table = 'Bookmark'

class LinkerRTMS(models.Model):
    sggCode = models.CharField(max_length=5, db_index=True)
    bjdName = models.CharField(max_length=10, db_index=True, null=True)
    bun = models.PositiveIntegerField(db_index=True)
    ji = models.PositiveIntegerField(db_index=True)
    kaptCode = models.CharField(max_length=16, null=True)

    class Meta:
        db_table = 'LinkerRTMS'

class RTMS(models.Model):
    reality = models.ForeignKey("Reality", on_delete=models.CASCADE, related_name='RTMSs')
    amount = models.CharField(max_length=41, null=True)
    year = models.CharField(max_length=4, null=True)
    month = models.CharField(max_length=2, null=True)
    day = models.CharField(max_length=6, null=True)
    useArea = models.FloatField(default=0.0)
    jibun = models.CharField(max_length=11, null=True)
    floor = models.CharField(max_length=4, null=True)
    cancelType = models.CharField(max_length=1, null=True)
    cancelDay = models.CharField(max_length=8, null=True)
    reqGBN = models.CharField(max_length=10, null=True)
    serialNumber = models.CharField(max_length=41, null=True)

    class Meta:
        db_table = 'RTMS'

class RTMSRent(models.Model):
    reality = models.ForeignKey("Reality", on_delete=models.CASCADE, related_name='RTMSRents')
    amount = models.CharField(max_length=41, null=True)
    rent = models.CharField(max_length=16, null=True)
    year = models.CharField(max_length=4, null=True)
    month = models.CharField(max_length=2, null=True)
    day = models.CharField(max_length=6, null=True)
    useArea = models.FloatField(default=0.0)
    jibun = models.CharField(max_length=11, null=True)
    floor = models.CharField(max_length=4, null=True)

    class Meta:
        db_table = 'RTMSRent'