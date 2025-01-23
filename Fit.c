#include <utility.h>
#include <formatio.h>
#include <ansi_c.h>
#include "Fit.h"
#include "Autotitration.h"

#define MAX 100
#define MA 4
#define SPREAD 0.001
//#define E0 0.594
//#define E0 1.0
#define V0 212.1947
#define NR_END 1
#define FREE_ARG char*
#define SWAP(a,b) {temp=(a);(a)=(b);(b)=temp;}
#define IA 16807
#define IM 2147483647
#define AM (1.0/IM)
#define IQ 127773
#define IR 2836
#define NTAB1 32
#define NDIV (1+(IM-1)/NTAB1)
#define EPS1 1.0e-4
#define EPS2 1.2E-7
#define RNMX (1.0-EPS2)
#define CON 1.4
#define CON2 (CON*CON)
#define BIG 1.0e30
#define NTAB2 10
#define SAFE 2.0

extern int mainhdl,sample,filehdl, fileok,ctrl,pnl,openc;
extern float am[];
extern float cellvol[];
extern char sumfilename[50],sumfile[MAX_PATHNAME_LEN]; 
extern int sit[36],sista[36],sicast[36],siniskin[36];
extern float sisal[36],sita[36],sitco2[36],siph[36];
extern char sidate[36][100],silat[36][100],silong[36][100];
extern char junk[300];
extern int crmb[100],crmindex,cellE0;
extern float crms[100],crmta[100],crmtco2[100],crmph[100];
extern double cellv,cellt,acidm,Sald;



void Fit(int flag, float Sal, double vol[],double emf[],int npts)

{ int popinfohdl;
  double E0;

  //if flag=0  use panel info
  //else use pop up
  
	long idum=(-911);
	int i, *ia,iter,itst,j,k,mfit=MA,nsample;
	double alamda,chisq,ochisq,*x,**covar,**alpha;
	double s,*consts,norm;
	double *h,*dif,*fit,*sig;
	static double a[MA+1]= {0.0,1.0,2.5/1000,2.3/1000,1.4};
	static double gues[MA+1]= {0.0,1.0,2.5e-3,2.3e-3,1.4e-6};
	
	consts=vector(1,17);
	h=vector(1,MAX);
	sig=vector(1,MAX);
	dif = vector(1,MAX);
	fit = vector(1,MAX);

/*      CALL CONSTANTS SUBROUTINE FOR EQUILIBRIUM CONSTANTS & TOTAL CONC. */

	/*GetCtrlVal (PNL_HNDL, CALC_CTEMP, &consts[14]);
	GetCtrlVal (PNL_HNDL, CALC_SAL, &consts[15]);
	GetCtrlVal (PNL_HNDL, CALC_CONC, &consts[16]);
	GetCtrlVal (PNL_HNDL, CALC_CVOL, &consts[17]);
	GetCtrlVal (PNL_HNDL, CALC_CAST, &CAST);
	GetCtrlVal (PNL_HNDL, CALC_PRINT_TOGGLE,&PRINT);
	GetCtrlVal (PNL_HNDL, CALC_PRESSURE, &pressure);
	GetCtrlVal (PNL_HNDL, CALC_INTEMP, &insitu);
	GetCtrlVal (PNL_HNDL, CALC_CELL,&CELL); */
	if (flag!=0){
	   popinfohdl = LoadPanel (0, "AutoTitration.uir", popinfo);
	   InstallPopup (popinfohdl);
	   SetCtrlVal(popinfohdl,popinfo_E0,cellE0);
	   SetCtrlVal(popinfohdl,popinfo_cellt,cellt);
	   SetCtrlVal(popinfohdl,popinfo_sal,Sald);
	   SetCtrlVal(popinfohdl,popinfo_acidm,acidm);
	   SetCtrlVal(popinfohdl,popinfo_cellv,cellv);
	   if (openc) SetCtrlAttribute(popinfohdl, popinfo_cellv, ATTR_LABEL_TEXT, "Cell W (g)");
	   else SetCtrlAttribute(popinfohdl, popinfo_cellv, ATTR_LABEL_TEXT, "Cell V (ml)");
	   ctrl=-1;
	   while(ctrl!=popinfo_panel && ctrl!= popinfo_pop){
	     GetUserEvent(1,&pnl,&ctrl);
	   }//end while
	   if (ctrl==popinfo_panel) flag=0; //go read panel info
	   else{
	      GetCtrlVal(popinfohdl,popinfo_E0,&cellE0);
	      GetCtrlVal(popinfohdl,popinfo_cellt,&consts[14]);
	      GetCtrlVal(popinfohdl,popinfo_sal,&consts[15]);
	      GetCtrlVal(popinfohdl,popinfo_acidm,&consts[16]);
	      GetCtrlVal(popinfohdl,popinfo_cellv,&consts[17]);
	   }
	   DiscardPanel (popinfohdl);
	}//end if flag
	if (flag==0){
	   GetCtrlVal(mainhdl,mainpnl_cellt,&consts[14]);
	   GetCtrlVal(mainhdl,mainpnl_ssal,&Sal);
	   Sald=Sal,consts[15]=Sal;
	   GetCtrlAttribute (mainhdl, mainpnl_aring, ATTR_CTRL_INDEX, &i);
	   consts[16]=am[i];
   	   GetCtrlAttribute (mainhdl, mainpnl_cring, ATTR_CTRL_INDEX, &i);
   	   consts[17]=cellvol[i];
       if (openc) GetCtrlVal(mainhdl, mainpnl_opencv,&junk[0]), consts[17] = atof(junk);//for open cells, this is the weight of sample
	}
	cnst(consts);


	for(i=1;i<=npts;i++)
	{

/*      CONVERT FROM VOLUME TO MASS UNITS AND FROM mVOLTS TO VOLTS      */

		vol[i]=vol[i]*(consts[11]);
		emf[i]=emf[i]/1000;
		sig[i]=.1/1000;
		E0=cellE0/1000.;
		
/*      CALCULATE [H+] USING INITIAL ESTIMATE OF E0 AND NERNST SLOPE    */

		h[i]=exp(-((E0 - emf[i])/consts[1])*log(10));
	}

/*      END OF DATA BLOCK ROUTINE                               */

/*      CONVERT FROM VOLUME TO MASS UNITS                       */

	/* Acid [] (consts[16]) should already be in mass units (mol/kg) so no need to convert anymore.
	consts[16]=consts[16]/consts[11]; */
	if (!openc) consts[17]=consts[17]*consts[10]; // if open cell, consts[10] is already weight in g
	
	ia=ivector(1,MA);
	covar=matrix(1,MA,1,MA);
	alpha=matrix(1,MA,1,MA);
	for (i=1;i<=mfit;i++) ia[i]=1;    /* fit with all parameters */
	for (i=1;i<=mfit;i++) a[i]=gues[i]; /* set initial values to gues[] */
	alamda=-1;
	mrqmin(vol,sig,npts,a,ia,MA,covar,alpha,&chisq,h,consts,dif,fit,hdelta,&alamda);
	k=1;
	itst=0;
	for (;;) {
		k++;
		ochisq=chisq;
		mrqmin(vol,sig,npts,a,ia,MA,covar,alpha,&chisq,h,consts,dif,fit,hdelta,&alamda);
		if (chisq > ochisq)
			itst=0;
		else if (fabs(ochisq-chisq) <1e-12)
			itst++;
		if (itst <4) continue;
		alamda=0.0;
		mrqmin(vol,sig,npts,a,ia,MA,covar,alpha,&chisq,h,dif,fit,consts,hdelta,&alamda);
		break;
	} //end for
	norm = 0.0;
	for(i=1;i<=npts;i++)
	{
		norm += dif[i]*dif[i];
		dif[i]=1e6*dif[i];
	}

	nsample=sample-8*((sample-1)/8);
	s=1e6*sqrt(norm/(npts-MA));
	a[2]=a[2]*1e6;
	a[3]=a[3]*1e6;
	Fmt(junk,"%d",nsample);
	SetCtrlAttribute(mainhdl,7*(nsample-1)+2,ATTR_LABEL_TEXT,junk);
	SetCtrlVal(mainhdl,7*(nsample-1)+2,consts[15]);
	SetCtrlVal(mainhdl,7*(nsample-1)+3,a[2]);
	SetCtrlVal(mainhdl,7*(nsample-1)+4,a[3]);
	SetCtrlVal(mainhdl,7*(nsample-1)+5,1000*(E0 - consts[1]*log(a[1])/log(10)));
	SetCtrlVal(mainhdl,7*(nsample-1)+6,-log(h[1]*a[1])/log(10));
	SetCtrlVal(mainhdl,7*(nsample-1)+7,-log(a[4])/log(10));
	SetCtrlVal(mainhdl,7*(nsample-1)+8,s);

	SetCtrlAttribute(mainhdl,7*(nsample-1)+2,ATTR_VISIBLE,1);
	for (i=1;i<=5;i++) SetCtrlAttribute(mainhdl,7*(nsample-1)+2+i,ATTR_VISIBLE,0);
	GetCtrlVal(mainhdl,mainpnl_tatco2ring,&i);
	SetCtrlAttribute(mainhdl,7*(nsample-1)+2+i,ATTR_VISIBLE,1);
	SetCtrlAttribute(mainhdl,7*(nsample-1)+8,ATTR_VISIBLE,1);

if(fileok!=0){
    if(fileok>2) Fmt(junk,"%s","Recalculation");
    else Fmt(junk,"%s",TimeStr());
	filehdl = OpenFile (sumfile, VAL_WRITE_ONLY, VAL_APPEND, VAL_ASCII);
    if(FindPattern (sumfilename, 0, -1, "All_station", 0, 0)>=0)
       FmtFile (filehdl, "%s<%s, %s, %s, %d, %d, %d, %s, %f[p3], %f[p1], %f[p2], %f[p2], %f[p2], %f[p3], %f[p3], %f[p2]\n",
         sidate[sample-1],silat[sample-1],silong[sample-1],sista[sample-1],sicast[sample-1],siniskin[sample-1],junk,consts[15],siph[sample-1],1000*(E0 - consts[1]*log(a[1])/log(10)),a[2],a[3],-log(h[1]*a[1])/log(10),-log(a[4])/log(10),s);
    if(FindPattern (sumfilename, 0, -1, "All_UW", 0, 0)>=0)
       FmtFile (filehdl, "%s<%s, %d, %s, %s, %s, %f[p3], %f[p2], %f[p2], %f[p2], %f[p3], %f[p3], %f[p2]\n", 
         sidate[sample-1],sista[sample-1],silat[sample-1],silong[sample-1],junk,consts[15],1000*(E0 - consts[1]*log(a[1])/log(10)),a[2],a[3],-log(h[1]*a[1])/log(10),-log(a[4])/log(10),s);
    if(FindPattern (sumfilename, 0, -1, "All_CRM", 0, 0)>=0)
       FmtFile (filehdl, "%s<%s, %d, %d, %f[p2], %f[p2], %f[p3], %s, %f[p3], %f[p2], %f[p2], %f[p2], %f[p3], %f[p3], %f[p2]\n", 
         sidate[sample-1],crmb[crmindex],sicast[sample-1],crmta[crmindex],crmtco2[crmindex],crmph[crmindex],junk,consts[15],1000*(E0 - consts[1]*log(a[1])/log(10)),a[2],a[3],-log(h[1]*a[1])/log(10),-log(a[4])/log(10),s);
    if(FindPattern (sumfilename, 0, -1, "All_test", 0, 0)>=0)
       FmtFile (filehdl, "%s<%s, %d, %s, %f[p3], %f[p2], %f[p2], %f[p2], %f[p3], %f[p3], %f[p2]\n", 
         sidate[sample-1],sista[sample-1],junk,consts[15],1000*(E0 - consts[1]*log(a[1])/log(10)),a[2],a[3],-log(h[1]*a[1])/log(10),-log(a[4])/log(10),s);
    
    CloseFile (filehdl);
}//end fileok

	free_matrix(alpha,1,MA,1,MA);
	free_matrix(covar,1,MA,1,MA);
	free_vector(h,1,MAX);
	free_vector(dif,1,MAX);
	free_vector(fit,1,MAX);
	free_vector(sig,1,MAX);
	free_vector(consts,1,17);
	free_ivector(ia,1,MA);
	exit;
}//end of calc2



void cnst(double consts[])

{
	double k,bt,st,ft,ks,kf,z,k1,k2,kb,kw,densw,dacid,ks1;
	double phinacl,phihcl,phimix,mtot,nacl,hcl,T,sqrts,half,I,t,sal;
	double a,b,c0,d0,na,h,cl,I0,E,M,pna,ph;

	T=consts[14]+273.15;
	t=consts[14];
	sal=consts[15];

	sqrts=sqrt(sal);
	I=19.92*sal/(1000-1.005*sal);

/*THEORETICAL NERNST SLOPE RT/F  R=J/mol K  and F=C/mol*/

	consts[1]=log(10)*8.31441*T/96484.56;

/*UPPSTROM, 1974  Total boron BT    mol/kg soln*/

	consts[2]=0.000232/10.81*(sal/1.80655);


/*MORRIS AND RILEY, 1966  Total sulfate ST   mol/kg soln*/

	st=0.1400/96.09*(sal/1.80655);
	consts[3]=st;

/*RILEY, 1965   Total fluoride FT         mol/kg soln      */

	ft=0.000067/18.9984*(sal/1.80655);
	consts[4]=ft;

/*DICKSON,1990 Dissociation of bisultate ion = mol/kg soln	  */

	ks = exp((-4276.1/T + 141.328 - 23.093*log(T) + (-13856/T +324.57 -
			47.986*log(T))*sqrt(I) + (35474/T -771.54 + 114.723*log(T))*I -
			2698/T*I*sqrt(I) + 1776/T*I*I) + log(1-sal*0.001005));


	consts[5]=ks;

/*DICKSON & RILEY, 1979 Dissociation of HF  = mol/kg soln*/

	kf=exp(1590.2/T - 12.641 + 1.525*sqrt(I) + log(1-sal*0.001005));


	consts[6]=kf;

	z=1 + st/ks + ft/kf;
	consts[7]=z;

/*DICKSON 1990 KB  = mol/ kg soln , [H]sws	*/

	consts[8] = exp((-8966.90 - 2890.53*sqrts - 77.942*sal +
					1.728*sal*sqrts - 0.0996*sal*sal)/T +
					(148.0248 + 137.1942*sqrts + 1.62142*sal) +
					(-24.4344 - 25.085*sqrts - 0.2474*sal)*log(T) +
					0.053105*sqrts*T +
					log((1 + st/ks + ft/kf)/(1 + st/ks)));

/*MILLERO, 1994	KWater	mol/kg soln*/

	consts[9] = exp(-13847.26/T + 148.96502 - 23.6521*log(T) +
					(118.67/T - 5.977 + 1.0495 *log(T))*sqrts -
					0.01615*sal);

/*ROY et al 1993  K1  mol/kg soln,REFIT FROM MILLERO 1994 [H]sws*/

	consts[13]=exp(3.17537 - 2329.1378/T - 1.597015*log(T) + (-0.210502
		- 5.79495/T)*sqrts + 0.0872208*sal -0.00684651*sal*sqrts);
		   
/*ROY et al 1993  K2  mol/kg soln,REFIT FROM MILLERO 1994 [H]sws*/

//	consts[12]=exp(-8.19754 - 3403.8782/T - 0.352253*log(T) + (-0.088885
//		- 25.95316/T)*sqrts + 0.1106658*sal - 0.00840155*sal*sqrts);

/* Replacing the above Roy equation with a new Mehrbach equation - 3/16/2001 */
/* Mehrbach et al 1973 K2  mol/kg soln, REFIT FROM DICKSON-MILLERO 1987 [H]sws */

	consts[12]=exp(-(1394.7/T + 4.777 - 0.0184*sal + 0.000118*sal*sal)*log(10));


/*      DENSITY OF SEAWATER MILLERO AND POISSON, 1981           */

	a = 8.24493e-4 - 4.0899e-6*(t) + 7.6438e-8*t*t - 8.2467e-10*t*t*t
		+ 5.3875e-12*t*t*t*t;

	b = -5.72466e-6 + 1.0227e-7*t - 1.6546e-9*t*t;

	c0 = 4.8314e-7;

	d0 = 0.999842594 + 6.793953e-5*t - 9.09529e-6*t*t + 1.001685e-7*t*t*t
			- 1.120083e-9*t*t*t*t + 6.536332e-12*t*t*t*t*t;

	consts[10] = d0 + a*sal + b*sal*sqrts + c0*sal*sal;


/*      DENSITY OF HCL ASSUMING TOTAL IONIC STRENGTH OF HCL AND NACL    */
/*      IS 0.7 FROM VOLUME OF MIXING CALCULATIONS                       */

	na=0.7-consts[16];
	h=consts[16];
	cl=0.7;

/*	CALCULATE THE IONIC STRENGTH TERMS									*/

	I0 = (na + cl + h)/2;

/*	CALCULATE THE TOTAL EQUIVALENTS AND EQUIVALENT FRACTIONS			*/

	E = (na + cl + h)/2;
	na = na/E;
	cl = cl/E;
	h = h/E;
	M = na*22.9898 + cl*35.453 + h*1.008;

/*	SODIUM SALTS FROM DENSITY EQUATIONS									*/

	nacl = (45.5655 - .2341*t +0.0034128*t*t -2.703e-5*t*t*t +
			1.4037e-7*t*t*t*t)*I0 + (-1.8527 + 0.053956*t -
			6.2635e-4*t*t)*I0*sqrt(I0) + (-1.6368 - 9.5653e-4*t +
			5.2829e-5*t*t)*I0*I0 +0.2274*I0*I0*sqrt(I0);

	nacl=(nacl/1000)+d0;
	phinacl=1000*(d0-nacl)/(I0*nacl*d0) + (22.9898 + 35.453)/nacl;

/*	HCL FROM DENSITY EQUATIONS											*/

	hcl = (20.3368 - 0.0737834 *t - 5.29257e-3*t*t + 4.50398e-4*t*t*t -
			1.17417e-5*t*t*t*t + 1.02433e-7*t*t*t*t*t)*I0
			- 1.46902*I0*sqrt(I0);
	hcl = hcl/1000 + d0;
	phihcl=1000*(d0-hcl)/(I0*hcl*d0) + (1.008 + 35.453)/hcl;

/*	PHIV OF THE MIXTURE				*/

	pna = phinacl*na*cl;
	ph = h*cl*phihcl;
	phimix = pna + ph;

	consts[11]=(M*E+1000)*d0*(1/(phimix*E*d0+1000));
	



/*      OUTPUT VALUES OF CONSTANTS TO DOUBLE CHECK EQUATIONS  */
/*
	printf("Output of constants for CNST.C program\n");
	printf("CONSTANT \t\tVALUE\n");
	printf("======== \t\t=====\n");
	printf("K=RT/F\t\t\t%f\n",consts[1]);
	printf("Total boron\t\t\t%f\n",consts[2]);
	printf("Total Sulfate\t\t\t%f\n",consts[3]);
	printf("Total Fluoride\t\t\t%f\n",consts[4]);
	printf("pKS1\t\t%f\n",-log(ks1)/log(10));
	printf("pK(HSO4)\t\t\t%f\n",-log(consts[5])/log(10));
	printf("lnK(HF)\t\t\t%f\n",-log(consts[6]));
	printf("Z=1+St/Ks+Ft/kf\t\t\t%f\n",consts[7]);
	printf("lnK1\t\t\t%f\n",-log(consts[13]));
	printf("lnK2\t\t\t%f\n",-log(consts[12]));
	printf("lnKB\t\t\t%f\n",log(consts[8]));
	printf("lnKW\t\t\t%f\n",-log(consts[9]));
	printf("DENSITY OF SEAWATER\t%f\n",consts[10]);
	printf("DENSITY OF ACID\t\t%f\n",consts[11]);
  */

}//end of cnst

void fgauss(double x, double a[], double *y, double dyda[], int na)
{
	int i;
	double fac,ex,arg;

	*y=0.0;
	for (i=1;i<=na-1;i+=3) {
	arg=(x-a[i+1])/a[i+2];
	ex=exp(-arg*arg);
	fac=a[i]*ex*2.0*arg;
	*y += a[i]*ex;
	dyda[i]=ex;
	dyda[i+1]=fac/a[1+2];
	dyda[i+2]=fac*arg/a[i+2];
    }
}//end of fgauss


void mrqcof(double vol[], double sig[], int ndata, double a[], int ia[],
   int ma, double **alpha, double beta[], double *chisq, double h[],
   double consts[], double dif[], double fit[],
   void (*funcs)(double, double, double [], double *, double [], double [],int))


{
	int i,j,k,l,m,mfit=0;
	double ymod,wt,sig2i,dy,*dyda;


	dyda=vector(1,ma);
	for (j=1;j<=ma;j++)
		if (ia[j]) mfit++;
	for (j=1;j<=mfit;j++)
	{
		for (k=1;k<=j;k++) alpha[j][k]=0.0;
		beta[j]=0.0;
	}
	*chisq=0.0;
	for (i=1;i<=ndata;i++)
	{

	       (*funcs)(h[i],vol[i],a,&ymod,dyda,consts,ma);
		sig2i=1.0/(sig[i]*sig[i]);
		dy=h[i]-ymod;
		dif[i]=dy;
		fit[i]=ymod;
		for (j=0,l=1;l<=ma;l++)
		{
			if (ia[l])
			{
				wt=dyda[l];
				for (j++,k=0,m=1;m<=l;m++)
					if (ia[m]) alpha[j][++k] +=
						wt*dyda[m];
				beta[j] +=dy*wt;
			}
		}
		*chisq +=dy*dy;
	}
	for (j=2;j<=mfit;j++)
		for (k=1;k<j;k++) alpha [k][j]=alpha[j][k];
	free_vector(dyda,1,ma);

}//end of mrqcof


void mrqmin(double vol[], double sig[], int ndata, double a[],
	int ia[],int ma, double **covar, double **alpha, double *chisq,
	double h[], double consts[], double dif[], double fit[],
     void (*funcs)(double, double,double [], double *, double [],double [],
	      int), double *alamda)

{
	int i,j,k,l,m;
	static int mfit;
	static double ochisq,*atry,*beta,*da,**oneda;

/*                      INITIALIZE SYSTEM PARAMETERS                    */

	if (*alamda <0.0)
	{
		atry=vector(1,ma);
		beta=vector(1,ma);
		da=vector(1,ma);
		for (mfit=0,j=1;j<=ma;j++)
			if (ia[j]) mfit++;
		oneda=matrix(1,mfit,1,1);
		*alamda=.001;

		mrqcof(vol,sig,ndata,a,ia,ma,alpha,beta,chisq,h,consts,dif,
			fit,funcs);

		ochisq=(*chisq);
		for (j=1;j<=ma;j++) atry[j]=a[j];
	}

/*                              END OF INITIALIZATION                   */

	for (j=0,l=1;l<=ma;l++)
	{
		if (ia[1])
		{
			for (j++,k=0,m=1;m<=ma;m++)
			{
				if (ia[m])
				{
					k++;
					covar[j][k]=alpha[j][k];
				}
			}
			covar[j][j]=alpha[j][j]*(1.0+(*alamda));
			oneda[j][1]=beta[j];
		}
	}
	gaussj(covar,mfit,oneda,1);

	for (j=1;j<=mfit;j++) da[j]=oneda[j][1];

/*              SET COVARIANCE & ALPHA MATRICES AFTER BEST FIT          */

	if (*alamda == 0.0)
	{
		covsrt(covar,ma,ia,mfit);
		free_matrix(oneda,1,mfit,1,1);
		free_vector(da,1,ma);
		free_vector(beta,1,ma);
		free_vector(atry,1,ma);
		return;
	}

/*              CYCLE UNTIL THE FITTING IS COMPLETE                     */

	for (j=0,l=1;l<=ma;l++)
		if (ia[l]) atry[l]=a[l]+da[++j];
	mrqcof(vol,sig,ndata,atry,ia,ma,covar,da,chisq,h,consts,dif,fit,
		funcs);
	if (*chisq < ochisq)
	{
		*alamda *= 0.1;
		ochisq=(*chisq);
		for (j=0,l=1;l<=ma;l++)
		{
			if (ia[l])
			{
				for (j++,k=0,m=1;m<=ma;m++)
				{
					if (ia[m])
					{
						k++;
						alpha[j][k]=covar[j][k];
					}
				}
				beta[j]=da[j];
				a[l]=atry[l];
			}
		}
	}
	else
	{
		*alamda *= 10.0;
		*chisq=ochisq;
	}
}//end of mrqmin



double func(double x,int par, double consts[], double ab[], double h, double v)

{
	int i;
	double ctmul,btmul,stmul,ftmul,allmul,dx,temp;
	temp=ab[par];
	ab[par]=x;


	ctmul = (ab[4]*ab[1]*h + 2*ab[4]*consts[12])/
		   (ab[1]*h*h + ab[4]*ab[1]*h + ab[4]*consts[12]);
	btmul = 1.0/(1 + (ab[1]*h)/consts[8]);
	stmul = (1-1/(1 + ab[1]*h/(consts[5]*consts[7])));
	ftmul = (1-1/(1 + ab[1]*h/(consts[6]*consts[7])));
	allmul = -consts[7]/(ab[1]*(consts[17] + v));
	dx=(allmul*(consts[17]*ab[2] - consts[17]*ab[3]*ctmul
		- consts[17]*consts[2]*btmul + consts[17]*consts[3]*stmul
		+ consts[17]*consts[4]*ftmul
		- (consts[17] + v)*consts[9]/(ab[1]*h) -v*consts[16]));
	ab[par]=temp;
	return dx;

}//end of func



double gasdev(long *idum)
{
	double ran1(long *idum);
	static int iset=0;
	static double gset;
	double fac,rsq,v1,v2;

	if (iset == 0)
	{
		do
		{
			v1=2.0*ran1(idum)-1.0;
			v2=2.0*ran1(idum)-1.0;
			rsq=v1*v1+v2*v2;
		}
		while (rsq >= 1.0 || rsq == 0.0);
		fac =sqrt(-2.0*log(rsq)/rsq);
		gset=v1*fac;
		iset=1;
		return v2*fac;
	}
	else
	{
		iset=0;
		return gset;
	}
}//end of gasdev



void gaussj(double **a, int n, double **b, int m)

{
	int *indxc, *indxr, *ipiv;
	int i, icol,irow, j,k,l,ll;
	double big,dum,pivinv,temp;

	indxc=ivector(1,n);
	indxr=ivector(1,n);
	ipiv=ivector(1,n);
	for (j=1;j<=n;j++) ipiv[j]=0;
	for (i=1;i<=n;i++)
	{
		big=0.0;
		for (j=1;j<=n;j++)
			if (ipiv[j] != 1)
				for (k=1;k<=n;k++)
				{
					if (ipiv[k] == 0)
					{
						if (fabs(a[j][k]) >= big)
						{
							big=fabs(a[j][k]);
							irow=j;
							icol=k;
						}
					}
					else if (ipiv[k] >1) nrerror("gaussj: Singular Matrix-1");
				}
		++(ipiv[icol]);
		if (irow != icol)
		{
			for (l=1;l<=n;l++) SWAP(a[irow][l],a[icol][l])
			for (l=1;l<=m;l++) SWAP(b[irow][l],b[icol][l])
		}
		indxr[i]=irow;
		indxc[i]=icol;
		if (a[icol][icol] == 0.0) nrerror("gaussf: Singular Matrix-2");
		pivinv=1.0/a[icol][icol];
		a[icol][icol]=1.0;
		for (l=1;l<=n;l++) a[icol][l] *= pivinv;
		for (l=1;l<=m;l++) b[icol][l] *= pivinv;
		for (ll=1;ll<=n;ll++)
			if (ll != icol)
			{
				dum=a[ll][icol];
				a[ll][icol]=0.0;
				for (l=1;l<=n;l++) a[ll][l] -= a[icol][l]*dum;
				for (l=1;l<=m;l++) b[ll][l] -= b[icol][l]*dum;
			}
	}
	for (l=n;l>=1;l--)
	{
		if (indxr[l] != indxc[l])
			for (k=1;k<=n;k++)
				SWAP(a[k][indxr[l]],a[k][indxc[l]]);
	}
	free_ivector(ipiv,1,n);
	free_ivector(indxr,1,n);
	free_ivector(indxc,1,n);
}//end of gaussj

void covsrt(double **covar, int ma, int ia[], int mfit)

{
	int i,j,k;
	double temp;

	for (i=mfit+1;i<=ma;i++)
		for (j=1;j<=i;j++) covar[i][j]=covar[j][i]=0.0;
	k=mfit;
	for (j=ma;j>=1;j--) {
		if (ia[j]) {
			for (i=1;i<=ma;i++) SWAP(covar[i][k], covar[i][j])
			for (i=1;i<=ma;i++) SWAP(covar[k][i],covar[j][i])
			k--;
		}
	}
}//end of covsrt

/*      PSEUDO-RANDOM NUMBER GENERATOR                                  */
double ran1(long *idum)
{
	int j;
	long k;
	static long iy=0;
	static long iv[NTAB1];
	double temp;

	if (*idum <= 0 || !iy)
	{
		if (-(*idum) < 1) *idum=1;
		else *idum = -(*idum);
		for (j=NTAB1+7;j>=0;j--)
		{
			k=(*idum)/IQ;
			*idum=IA*(*idum-k*IQ)-IR*k;
			if (*idum < 0) *idum +=IM;
			if (j < NTAB1) iv[j] = *idum;
		}
		iy=iv[0];
	}
	k=(*idum)/IQ;
	*idum=IA*(*idum-k*IQ)-IR*k;
	if (*idum < 0) *idum += IM;
	j=iy/NDIV;
	iy=iv[j];
	iv[j] = *idum;
	if ((temp=AM*iy) > RNMX) return RNMX;
	else return temp;
}//end of ran1


double dfridr(double (*func)(double, int, double [], double [], double, double),
	double x, double hs, int par,double *err,
		double consts[], double h, double vol, double ab[])

{
	int i,j;
	double errt,fac,hh,**a,ans;

	if(hs == 0.0) nrerror("h must be nonzero in dfridr.");
	a=matrix(1,NTAB2,1,NTAB2);
	hh=hs;
	a[1][1]=((*func)(x+hh,par,consts,ab,h,vol)
		- (*func)(x-hh,par,consts,ab,h,vol))/(2.0*hh);

	*err=BIG;
	for (i=2;i<=NTAB2;i++)
	{
		hh /= CON;
		a[1][i] = ((*func)(x+hh,par,consts,ab,h,vol) - (*func)(x-hh,par,consts,ab,h,vol))/(2.0*hh);
		fac=CON2;
		for (j=2;j<=i;j++)
		{
			a[j][i]=(a[j-1][i]*fac-a[j-1][i-1])/(fac-1.0);
			fac=CON2*fac;
			errt=FMAX(fabs(a[j][i]-a[j-1][i]),fabs(a[j][i]-a[j-1][i-1]));
			if (errt <= *err)
			{
				*err=errt;
				ans=a[j][i];
			}
		}
		if (fabs(a[i][i]-a[i-1][i-1]) >= SAFE*(*err)) break;
	}
	free_matrix(a,1,NTAB2,1,NTAB2);
	return ans;
}//end of dfridr


void hdelta(double h, double vol,  double a[], double *y, double dyda[],
	double consts[], int ma)

{
	int i;
	double ctmul,btmul,stmul,ftmul,allmul,x,err;
	double hs[5] = {0.0,0.1, 1e-3,1e-3,1e-7};

	*y=0.0;

	ctmul = consts[17]*(a[4]*a[1]*h + 2*a[4]*consts[12])/
		   (a[1]*a[1]*h*h + a[4]*a[1]*h + a[4]*consts[12]);

	btmul = consts[17]*(1/(1 + (a[1]*h)/consts[8]));

	stmul = consts[17]*(1-1/(1 + a[1]*h/(consts[5]*consts[7])));

	ftmul = consts[17]*(1-1/(1 + a[1]*h/(consts[6]*consts[7])));

	allmul = - consts[7]/(a[1]*(consts[17] + vol));

	*y += allmul*(consts[17]*a[2] - a[3]*ctmul -
		consts[2]*btmul + consts[3]*stmul + consts[4]*ftmul
		- (consts[17] + vol)*consts[9]/(a[1]*h)-vol*consts[16]);



	for(i=1;i<=ma;i++)
	{
		x=a[i];
		dyda[i]=dfridr(hder,x,hs[i],i,&err,consts,h,vol,a);

	 }

}//end of hdelta


void fdjac(int n,double x[], double fvec[], double **df,
		void(*vecfunc)(int, double [], double []))

{
	int i,j;
	double h,temp,*f;

	f=vector(1,n);
	for (j=1;j<=n;j++)
	{
		temp=x[j];
		h=EPS2*fabs(temp);
		if (h == 0.0) h=EPS2;
		x[j]=temp+h;
		h=x[j]-temp;
		(*vecfunc)(n,x,f);
		x[j]=temp;
		for (i=1;i<=n;i++) df[i][j]=(f[i]-fvec[i])/h;
	}
	free_vector(f,1,n);
}//end of fdjac

double hder(double x,int par, double consts[], double ab[], double h, double v)

{
	int i;
	double ctmul,btmul,stmul,ftmul,allmul,dx,temp;
	temp=ab[par];
	ab[par]=x;

	ctmul = consts[17]*(ab[4]*ab[1]*h + 2*ab[4]*consts[12])/
		   (ab[1]*ab[1]*h*h + ab[4]*ab[1]*h + ab[4]*consts[12]);
	btmul = consts[17]/(1 + (ab[1]*h)/consts[8]);
	stmul = consts[17]*(1-1/(1 + ab[1]*h/(consts[5]*consts[7])));
	ftmul = consts[17]*(1-1/(1 + ab[1]*h/(consts[6]*consts[7])));
	allmul = - consts[7]/(ab[1]*(consts[17] + v));
	dx = allmul*(consts[17]*ab[2] - ab[3]*ctmul -
		consts[2]*btmul + consts[3]*stmul + consts[4]*ftmul
		- (consts[17] + v)*consts[9]/(ab[1]*h)-v*consts[16]);

	ab[par]=temp;
	return dx;


}//end of hder


//************** NRUTIL ************************************

void nrerror(char error_text[])
/* Numerical Recipes standard error handler */
{
	//fprintf(stderr,"Numerical Recipes run-time error...\n");
	//fprintf(stderr,"%s\n",error_text);
	//fprintf(stderr,"...now exiting to system...\n");
	//exit(1);
}
double *vector(long nl, long nh)
/* allocate a double vector with subscript range v[n1..nh] */
{
	double *v;

	v=(double *)malloc((size_t) ((nh-nl+1+NR_END)*sizeof(double)));
	if (!v) nrerror("allocation failure in vector()");
	return v;
}
int *ivector(long nl,long nh)
{

	int *v;

	v=(int *)malloc((size_t) ((nh-nl+1+NR_END)*sizeof(int)));
	if (!v) nrerror("allocation failure in ivector()");
	return v;
}
double **matrix(long nrl, long nrh, long ncl, long nch)
/* allocate a double matrix with subscript range m[nrl..nrh][ncl..nch] */
{
	long i,nrow=nrh-nrl+1,ncol=nch-ncl+1;
	double **m;

	/* allocate pointer to rows */
	m=(double **) malloc((size_t)((nrow+NR_END)*sizeof(double*)));
	if (!m) nrerror("allocation failure 1 in matrix()");
	m += NR_END;
	m -= nrl;

	/* allocate rows and set pointer to them */
	m[nrl]=(double *) malloc((size_t)((nrow*ncol+NR_END)*sizeof(double)));

	if (!m[nrl]) nrerror("allocation failure 2 in matrix()");
	m[nrl] += NR_END;
	m[nrl] -= ncl;

	for(i=nrl+1;i<=nrh;i++) m[i]=m[i-1]+ncol;

	/* return pointer to array of pointer to rows */
	return m;
}
void free_vector(double *v,long nl, long nh)
/* free a double vectore alocated with vector () */

{
	free((FREE_ARG) (v+nl-NR_END));
}
void free_ivector(int *v, long nl, long nh)
/* free a int vectore alocated with vector () */
{
	free((FREE_ARG) (v+nl-NR_END));
}
void free_matrix(double **m, long nrl, long nrh, long ncl, long nch)
/* free afloat matrix allocated by matrix() */
{
	free((FREE_ARG) (m[nrl]+ncl-NR_END));
	free ((FREE_ARG) (m+nrl-NR_END));
}


