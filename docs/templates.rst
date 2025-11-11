Templates
=========

|bfrescox| works by using templates to generate input files for |frescox| runs.
For certain problems, |bfrescox| can generate templates automatically based on a
user's problem specification (see the examples for more examples of
generating and using templates). However, |bfrescox| also allows users to create
their own templates, and, whether the template was generated automatically or
created by the user, |bfrescox| fills them in and runs |frescox| with them the
same way.

The way templates work is simple: take any existing |frescox| input file, and
replace any values you want with keys of the following format: "@key_name@". The
set of such replacements constitutes the set of parameters one can vary. For
example, consider the following simple |frescox| input file:

.. code-block:: 

  p+Ni78 Coulomb + Nuclear
  NAMELIST
  &FRESCO hcm=0.1 rmatch=60.0
      jtmin=0.0 jtmax=60.0 absend= 0.01
    thmin=0.00 thmax=180.00 thinc=1.00
      iter=0 ips=0.0 iblock=0 chans=1 smats=2  xstabl=1
    wdisk=2
      elab(1)=50.0 treneg=1 /

   &PARTITION namep='projectile' massp=1 zp=1
              namet='target'   masst=78 zt=28 qval=-0.000 nex=1  /
   &STATES jp=0.5 bandp=1 ep=0.0000 cpot=1 jt=0.0 bandt=1 et=0.0 /
   &partition /

   &POT kp=1 ap=1 at=78 rc=1.2  /
   &POT kp=1 type=1  p1=@V@ p2=@r@ p3=@a@ p4=@W@ p5=@rw@ p6=@aw@ /
   &POT kp=1 type=2  p1=@Vs@ p2=@rs@ p3=@as@ p4=@Ws@ p5=@rws@ p6=@aws@ /
   &POT kp=1 type=3  p1=@Vso@ p2=@rso@ p3=@aso@ p4=@Wso@ p5=@rwso@ p6=@awso@ /

   &pot /
   &overlap /
   &coupling /

This template file is identical to a normal |frescox| input file, except that
the parameters of the optical potential have been replaced with keys of the form
"@key_name@". When |bfrescox| fills in this template, it will replace these keys
with actual numerical values provided by the user. One could just as easily add
a key for the projectile energy, number of angular steps, or any other |frescox|
input parameter.


The `Configuration` class encapsulates a particular |frescox| input
configuration. `Configuration.from_template` reads in a file like the one above,
allows the user to pass in a python `dict` mapping keys to values to fill in the
template, and writes the output. For example:

.. code-block:: python

   from bfrescox import Configuration

   template_file = "path/to/ni78.template"
   parameters = {
       "V": 50.0,
       "r": 1.25,
       "a": 0.65,
       "W": 10.0,
       # ... etc ...
   }

   config = Configuration.from_template(template_file, "ni78.nml",  parameters)

See the examples for more details on using and generating templates with |bfrescox|.
