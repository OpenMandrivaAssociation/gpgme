/* PGO trainer for GPGME.
 *
 * Models a long-lived mail / key-manager client: one context, many
 * encrypt / decrypt / sign / verify / keylist / export operations on
 * mail-sized and attachment-sized buffers.  Expects the tests/gpg
 * demo keyring and passphrase "abc".
 */

#include <errno.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <gpgme.h>

#define ALFA  "A0FF4590BB6122EDEF6E3C542D727CC768697734"
#define BRAVO "D695676BDCEDCC2CDD6152BCFE180B1DA9E3B0B2"

static void
die (gpgme_error_t err, const char *what)
{
  fprintf (stderr, "pgo-train: %s: %s\n", what, gpgme_strerror (err));
  exit (1);
}

static gpgme_error_t
passphrase_cb (void *opaque, const char *uid_hint, const char *info,
	       int last_was_bad, int fd)
{
  const char pass[] = "abc\n";
  size_t off = 0, len = sizeof (pass) - 1;
  ssize_t n;

  (void) opaque;
  (void) uid_hint;
  (void) info;
  (void) last_was_bad;

  while (off < len)
    {
      n = gpgme_io_write (fd, pass + off, len - off);
      if (n <= 0)
	return gpgme_error_from_errno (errno);
      off += (size_t) n;
    }
  return 0;
}

static void
fill_mail (char *buf, size_t n)
{
  static const char body[] =
    "From: Alice <alfa@example.net>\n"
    "To: Bob <bravo@example.net>\n"
    "Subject: GPGME PGO training message\n"
    "\n"
    "This is a typical mailed paragraph used to train GPGME's data\n"
    "pump and status parser rather than a 12-byte unit test.\n";
  size_t i, bl = sizeof (body) - 1;

  for (i = 0; i < n; i++)
    buf[i] = body[i % bl];
}

static void
keylist (gpgme_ctx_t ctx, int secret)
{
  gpgme_error_t err;
  gpgme_key_t key;

  err = gpgme_op_keylist_start (ctx, NULL, secret);
  if (err)
    die (err, "keylist_start");
  while (!(err = gpgme_op_keylist_next (ctx, &key)))
    {
      gpgme_user_id_t uid;
      gpgme_subkey_t sub;

      for (uid = key->uids; uid; uid = uid->next)
	(void) uid->email;
      for (sub = key->subkeys; sub; sub = sub->next)
	(void) sub->fpr;
      gpgme_key_unref (key);
    }
  if (gpgme_err_code (err) != GPG_ERR_EOF)
    die (err, "keylist_next");
  err = gpgme_op_keylist_end (ctx);
  if (err)
    die (err, "keylist_end");
}

static void
export_key (gpgme_ctx_t ctx, const char *pattern)
{
  gpgme_error_t err;
  gpgme_data_t out;

  err = gpgme_data_new (&out);
  if (err)
    die (err, "data_new export");
  err = gpgme_op_export (ctx, pattern, 0, out);
  if (err)
    die (err, "export");
  gpgme_data_release (out);
}

static void
cycle (gpgme_ctx_t ctx, gpgme_key_t recp[], char *buf, size_t size, int armor)
{
  gpgme_error_t err;
  gpgme_data_t in, cipher, plain, sig;
  gpgme_encrypt_flags_t eflags = GPGME_ENCRYPT_ALWAYS_TRUST;

  gpgme_set_armor (ctx, armor);
  gpgme_set_textmode (ctx, armor);

  err = gpgme_data_new_from_mem (&in, buf, size, 0);
  if (err)
    die (err, "data_new_from_mem");
  err = gpgme_data_new (&cipher);
  if (err)
    die (err, "data_new cipher");

  err = gpgme_op_encrypt (ctx, recp, eflags, in, cipher);
  if (err)
    die (err, "encrypt");
  (void) gpgme_data_identify (cipher, 0);

  err = gpgme_data_seek (cipher, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek cipher");
  err = gpgme_data_new (&plain);
  if (err)
    die (err, "data_new plain");
  err = gpgme_op_decrypt (ctx, cipher, plain);
  if (err)
    die (err, "decrypt");
  gpgme_data_release (plain);
  gpgme_data_release (cipher);

  err = gpgme_data_seek (in, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek in");
  err = gpgme_data_new (&sig);
  if (err)
    die (err, "data_new sig");
  err = gpgme_op_sign (ctx, in, sig, GPGME_SIG_MODE_NORMAL);
  if (err)
    die (err, "sign");

  err = gpgme_data_seek (sig, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek sig");
  err = gpgme_data_new (&plain);
  if (err)
    die (err, "data_new verify");
  err = gpgme_op_verify (ctx, sig, NULL, plain);
  if (err)
    die (err, "verify");
  gpgme_data_release (plain);
  gpgme_data_release (sig);

  err = gpgme_data_seek (in, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek in detach");
  err = gpgme_data_new (&sig);
  if (err)
    die (err, "data_new detach");
  err = gpgme_op_sign (ctx, in, sig, GPGME_SIG_MODE_DETACH);
  if (err)
    die (err, "sign detach");
  err = gpgme_data_seek (sig, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek detach");
  err = gpgme_data_seek (in, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek in verify-detach");
  err = gpgme_op_verify (ctx, sig, in, NULL);
  if (err)
    die (err, "verify detach");
  gpgme_data_release (sig);

  err = gpgme_data_seek (in, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek in encsign");
  err = gpgme_data_new (&cipher);
  if (err)
    die (err, "data_new encsign");
  err = gpgme_op_encrypt_sign (ctx, recp, eflags, in, cipher);
  if (err)
    die (err, "encrypt_sign");
  err = gpgme_data_seek (cipher, 0, SEEK_SET);
  if (err)
    die (gpgme_err_code_from_errno (errno), "seek encsign");
  err = gpgme_data_new (&plain);
  if (err)
    die (err, "data_new decverify");
  err = gpgme_op_decrypt_verify (ctx, cipher, plain);
  if (err)
    die (err, "decrypt_verify");

  gpgme_data_release (plain);
  gpgme_data_release (cipher);
  gpgme_data_release (in);
}

int
main (void)
{
  gpgme_error_t err;
  gpgme_ctx_t ctx;
  gpgme_key_t alfa = NULL, bravo = NULL, recp[3];
  struct
  {
    size_t size;
    int reps;
    int armor;
  } jobs[] = {
    { 4096,   30, 1 },	/* short inline PGP mail */
    { 16384,  16, 1 },	/* typical MIME body */
    { 65536,   8, 0 },	/* long thread, binary */
    { 262144,  4, 0 },	/* small attachment */
  };
  unsigned i, j;
  char *buf;

  gpgme_check_version (NULL);
  setlocale (LC_ALL, "");
  gpgme_set_locale (NULL, LC_CTYPE, setlocale (LC_CTYPE, NULL));

  err = gpgme_engine_check_version (GPGME_PROTOCOL_OpenPGP);
  if (err)
    die (err, "engine_check_version");

  err = gpgme_new (&ctx);
  if (err)
    die (err, "gpgme_new");

  gpgme_set_pinentry_mode (ctx, GPGME_PINENTRY_MODE_LOOPBACK);
  gpgme_set_passphrase_cb (ctx, passphrase_cb, NULL);

  err = gpgme_get_key (ctx, ALFA, &alfa, 0);
  if (err)
    die (err, "get_key alfa");
  err = gpgme_get_key (ctx, BRAVO, &bravo, 0);
  if (err)
    die (err, "get_key bravo");
  recp[0] = alfa;
  recp[1] = bravo;
  recp[2] = NULL;

  /* Address-book style lookup, then the listings Kleopatra does. */
  {
    gpgme_key_t bymail = NULL;

    err = gpgme_get_key (ctx, "alfa@example.net", &bymail, 0);
    if (err)
      die (err, "get_key by mail");
    gpgme_key_unref (bymail);
  }
  keylist (ctx, 0);
  keylist (ctx, 1);

  err = gpgme_signers_add (ctx, alfa);
  if (err)
    die (err, "signers_add");

  for (i = 0; i < sizeof jobs / sizeof jobs[0]; i++)
    {
      buf = malloc (jobs[i].size);
      if (!buf)
	{
	  perror ("malloc");
	  return 1;
	}
      fill_mail (buf, jobs[i].size);
      for (j = 0; j < (unsigned) jobs[i].reps; j++)
	{
	  cycle (ctx, recp, buf, jobs[i].size, jobs[i].armor);
	  if (j % 3 == 0)
	    {
	      keylist (ctx, 0);
	      keylist (ctx, 1);
	    }
	}
      free (buf);
    }

  for (i = 0; i < 8; i++)
    export_key (ctx, ALFA);

  gpgme_key_unref (alfa);
  gpgme_key_unref (bravo);
  gpgme_release (ctx);
  return 0;
}
